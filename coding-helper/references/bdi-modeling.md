# Formal BDI Modeling

Use this reference to represent beliefs, desires, intentions, plans, provenance, and temporal validity as RDF, OWL, and SPARQL. The model is symbolic and can be parsed, reasoned over, and validated entirely with local ontology tooling. This reference adds modeling guidance only; process and authorization are governed by [`../SKILL.md`](../SKILL.md).

## Modeling Boundary

Keep four categories distinct:

| Category | Examples | Semantics |
|---|---|---|
| World | `WorldState`, observations | Agent-independent state being described |
| Mental state | `Belief`, `Desire`, `Intention` | Persistent cognitive attitude |
| Mental process | belief formation, deliberation, commitment | Event that creates or changes a mental state |
| Planning | `Goal`, `Plan`, `Task`, `Action` | Description and execution of intended change |

A belief is not the world state it refers to. A desire is not yet a commitment. An intention commits to a desire and specifies a plan. A task is part of a plan; an action is an execution of a task.

## Minimal Vocabulary

Core classes:

- `Agent`, `WorldState`;
- `MentalState` with subclasses `Belief`, `Desire`, `Intention`;
- `MentalProcess` with subclasses `BeliefProcess`, `DesireProcess`, `IntentionProcess`;
- `Goal`, `Plan`, `Task`, `Action`, `PlanExecution`;
- `Justification`, `TimeInterval`.

Core object properties:

| Property | Domain | Range | Purpose |
|---|---|---|---|
| `hasMentalState` | Agent | MentalState | State ownership |
| `refersTo` | Belief | WorldState | Belief grounding |
| `isMotivatedBy` | Desire | Belief | Motivational support |
| `fulfils` | Intention | Desire | Commitment target |
| `isSupportedBy` | Intention | Belief | Feasibility or evidential support |
| `specifies` | Intention | Plan | Intended course |
| `hasComponent` | Plan | Task | Plan decomposition |
| `precedes` | Task | Task | Partial ordering |
| `isExecutionOf` | Action | Task | Execution link |
| `generates` | MentalProcess | MentalState | State formation |
| `modifies` | MentalProcess | MentalState | State revision |
| `bringsAbout` | Action or PlanExecution | WorldState | Resulting state |
| `isJustifiedBy` | MentalState | Justification | Provenance |
| `hasValidity` | MentalState | TimeInterval | Temporal scope |

Use inverse properties only when the query workload benefits from them. If declared, define them with `owl:inverseOf` rather than maintaining two unrelated predicates.

## OWL Core

The following fragment expresses inference semantics. Standard namespace IRIs are identifiers; loading schemas from the network is not required.

```turtle
@prefix bdi: <urn:example:bdi:> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

bdi:MentalState a owl:Class .
bdi:Belief a owl:Class ; rdfs:subClassOf bdi:MentalState .
bdi:Desire a owl:Class ; rdfs:subClassOf bdi:MentalState .
bdi:Intention a owl:Class ; rdfs:subClassOf bdi:MentalState .
bdi:WorldState a owl:Class .
bdi:Plan a owl:Class .
bdi:Justification a owl:Class .

bdi:Belief owl:disjointWith bdi:Desire, bdi:Intention .
bdi:Desire owl:disjointWith bdi:Intention .

bdi:refersTo a owl:ObjectProperty ;
    rdfs:domain bdi:Belief ;
    rdfs:range bdi:WorldState .

bdi:isMotivatedBy a owl:ObjectProperty ;
    rdfs:domain bdi:Desire ;
    rdfs:range bdi:Belief .

bdi:fulfils a owl:ObjectProperty ;
    rdfs:domain bdi:Intention ;
    rdfs:range bdi:Desire .

bdi:specifies a owl:ObjectProperty ;
    rdfs:domain bdi:Intention ;
    rdfs:range bdi:Plan .

bdi:isJustifiedBy a owl:ObjectProperty ;
    rdfs:domain bdi:MentalState ;
    rdfs:range bdi:Justification .

bdi:Belief rdfs:subClassOf [
    a owl:Restriction ;
    owl:onProperty bdi:refersTo ;
    owl:someValuesFrom bdi:WorldState
] .

bdi:Desire rdfs:subClassOf [
    a owl:Restriction ;
    owl:onProperty bdi:isMotivatedBy ;
    owl:someValuesFrom bdi:Belief
] .

bdi:Intention rdfs:subClassOf [
    a owl:Restriction ;
    owl:onProperty bdi:fulfils ;
    owl:qualifiedCardinality "1"^^xsd:nonNegativeInteger ;
    owl:onClass bdi:Desire
] , [
    a owl:Restriction ;
    owl:onProperty bdi:specifies ;
    owl:someValuesFrom bdi:Plan
] .
```

OWL uses the open-world assumption. Existential and cardinality restrictions support inference and consistency checking but do not, by themselves, report every missing triple as invalid data. Use explicit SPARQL validation queries for closed-world ingestion requirements.

## Grounded Cognitive Chain

Keep the world-to-belief and belief-to-action provenance explicit:

```turtle
@prefix bdi: <urn:example:bdi:> .
@prefix ex: <urn:example:instance:> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:agentA a bdi:Agent ;
    bdi:hasMentalState ex:beliefRouteBlocked,
                       ex:desireArrive,
                       ex:intentionDetour .

ex:blockedRoad a bdi:WorldState .

ex:beliefRouteBlocked a bdi:Belief ;
    bdi:refersTo ex:blockedRoad ;
    bdi:isJustifiedBy ex:observation17 ;
    bdi:hasValidity ex:intervalMorning .

ex:desireArrive a bdi:Desire ;
    bdi:isMotivatedBy ex:beliefRouteBlocked .

ex:intentionDetour a bdi:Intention ;
    bdi:fulfils ex:desireArrive ;
    bdi:isSupportedBy ex:beliefRouteBlocked ;
    bdi:specifies ex:detourPlan .

ex:detourPlan a bdi:Plan ;
    bdi:hasComponent ex:turnEast, ex:rejoinRoute .

ex:turnEast a bdi:Task ; bdi:precedes ex:rejoinRoute .
ex:rejoinRoute a bdi:Task .

ex:observation17 a bdi:Justification .
ex:intervalMorning a bdi:TimeInterval ;
    bdi:hasStart "2026-07-27T08:00:00Z"^^xsd:dateTime ;
    bdi:hasEnd "2026-07-27T10:00:00Z"^^xsd:dateTime .
```

Do not use free text as the only grounding. Labels and comments explain an individual, while object properties preserve queryable semantics.

## Mental Processes And Revision

Represent state transitions as individuals when auditability matters:

```turtle
ex:observationProcess17 a bdi:BeliefProcess ;
    bdi:reasonsUpon ex:blockedRoad ;
    bdi:generates ex:beliefRouteBlocked ;
    bdi:occurredAt "2026-07-27T08:03:00Z"^^xsd:dateTime .

ex:revisionProcess18 a bdi:BeliefProcess ;
    bdi:reasonsUpon ex:roadCleared ;
    bdi:modifies ex:beliefRouteBlocked ;
    bdi:generates ex:beliefRouteOpen .
```

Prefer creating a new versioned belief and closing the prior validity interval when historical truth matters. In-place mutation is suitable only when history is intentionally out of scope.

For composite beliefs, use `hasPart` only when parts can be independently queried, justified, or revised. Avoid turning every predicate into a separate belief individual.

## Temporal Semantics

Choose one interval policy and document it. Half-open intervals `[start, end)` avoid double validity at adjacent boundaries. An active-state query then uses:

```sparql
PREFIX bdi: <urn:example:bdi:>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?state WHERE {
  ?state a bdi:MentalState ;
         bdi:hasValidity ?interval .
  ?interval bdi:hasStart ?start .
  OPTIONAL { ?interval bdi:hasEnd ?end }
  BIND("2026-07-27T09:00:00Z"^^xsd:dateTime AS ?at)
  FILTER(?start <= ?at && (!BOUND(?end) || ?at < ?end))
}
```

An absent end can represent current validity. Do not use it to mean both "unknown end" and "unbounded end" without an explicit status property.

## Triples To Beliefs To Triples

A deterministic bidirectional pipeline has four stages:

1. Parse RDF and identify world-state assertions and provenance.
2. Apply explicit mapping rules that create belief and mental-process instances.
3. Run ontology inference and local deliberation rules to select supported desires, intentions, and plans.
4. Record executed actions and resulting world states as new RDF with provenance and timestamps.

Keep source assertions separate from inferred assertions by named graph or provenance property. Never overwrite the observation graph with conclusions.

## SPARQL Competency Queries

Trace the complete support chain for an intention:

```sparql
PREFIX bdi: <urn:example:bdi:>

SELECT ?intention ?desire ?belief ?world ?plan WHERE {
  ?intention a bdi:Intention ;
             bdi:fulfils ?desire ;
             bdi:isSupportedBy ?belief ;
             bdi:specifies ?plan .
  ?desire bdi:isMotivatedBy ?belief .
  ?belief bdi:refersTo ?world .
}
```

Retrieve direct task ordering edges for a plan:

```sparql
PREFIX bdi: <urn:example:bdi:>

SELECT ?task ?next WHERE {
  ?plan a bdi:Plan ; bdi:hasComponent ?task .
  OPTIONAL { ?task bdi:precedes ?next }
}
```

Do not assume lexical ordering of task IRIs is execution order. For a strict sequence, validate one start node, one end node, no cycles, and one connected path. For partial-order plans, preserve the graph and compute only currently enabled tasks.

## Closed-World Validation

Find beliefs with no world-state grounding:

```sparql
PREFIX bdi: <urn:example:bdi:>

SELECT ?belief WHERE {
  ?belief a bdi:Belief .
  FILTER NOT EXISTS {
    ?belief bdi:refersTo ?world .
    ?world a bdi:WorldState .
  }
}
```

Find intentions that do not fulfil exactly one desire:

```sparql
PREFIX bdi: <urn:example:bdi:>

SELECT ?intention (COUNT(DISTINCT ?desire) AS ?count) WHERE {
  ?intention a bdi:Intention .
  OPTIONAL { ?intention bdi:fulfils ?desire }
}
GROUP BY ?intention
HAVING (COUNT(DISTINCT ?desire) != 1)
```

Find unsupported intentions or missing plans:

```sparql
PREFIX bdi: <urn:example:bdi:>

SELECT ?intention WHERE {
  ?intention a bdi:Intention .
  FILTER (
    NOT EXISTS { ?intention bdi:isSupportedBy ?belief }
    || NOT EXISTS { ?intention bdi:specifies ?plan }
  )
}
```

Run parse checks, ontology consistency checks, and closed-world queries as separate gates. A graph can be valid Turtle yet violate the domain model; an OWL ontology can be consistent while required application fields are absent.

## Modeling Checklist

- World states remain distinct from beliefs about those states.
- Beliefs have grounding, provenance, ownership, and temporal scope where needed.
- Desires cite motivating beliefs.
- Intentions fulfil a desire, cite supporting beliefs, and specify a plan.
- Plans contain tasks; actions point to the tasks they execute.
- Process individuals preserve formation and revision history when required.
- Inverse properties, cardinalities, and disjointness are declared intentionally.
- Interval boundary semantics and open-ended validity are documented.
- Competency queries answer the questions the ontology was built to support.
- Validation queries cover missing links, cardinality, ordering, cycles, and temporal conflicts.
- Parsing, inference, validation, and serialization run with local deterministic tooling and fixtures.

