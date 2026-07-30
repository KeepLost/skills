# Graphics And Shaders

Use this compact reference to route shader work and to avoid common GLSL ES 3.00 and WebGL2 failures. Process and authorization are governed by [`../SKILL.md`](../SKILL.md).

## Technique Index

| Goal | Primary technique | Common companions |
|---|---|---|
| Mathematical 2D shapes | Signed distance fields | Analytical antialiasing, palettes |
| Implicit 3D scenes | Sphere tracing | SDF composition, normals, lighting |
| Repeated or organic geometry | Domain transforms | Noise, bounded repetition |
| Terrain and water | Height fields or displaced surfaces | Normals, fog, reflections |
| Smoke, clouds, fire | Volume integration | Density fields, early termination |
| Particles and cellular effects | Stateful textures | Ping-pong framebuffers |
| Bloom, grading, distortion | Post-processing pass | HDR targets, tone mapping |
| Persistent simulation | Multipass rendering | Fixed timestep, boundary handling |
| Debugging | Diagnostic outputs | Compile logs, reduced loop budgets |

Choose the smallest pipeline that can express the effect. A fragment-only pass is preferable to multipass state; analytic intersections are preferable to ray marching when the geometry has a stable closed-form solution.

## WebGL2 Contract

Use a WebGL2 context and GLSL ES 3.00 shaders. The version directive must be the first line of each shader source.

```glsl
#version 300 es
const vec2 POSITIONS[3] = vec2[3](
    vec2(-1.0, -1.0),
    vec2( 3.0, -1.0),
    vec2(-1.0,  3.0)
);

void main() {
    gl_Position = vec4(POSITIONS[gl_VertexID], 0.0, 1.0);
}
```

```glsl
#version 300 es
precision highp float;

uniform vec2 uResolution;
uniform float uTime;
out vec4 outColor;

void main() {
    vec2 uv = (2.0 * gl_FragCoord.xy - uResolution) / uResolution.y;
    vec3 color = vec3(0.5 + 0.5 * cos(uTime + uv.xyx + vec3(0.0, 2.0, 4.0)));
    outColor = vec4(color, 1.0);
}
```

Stable conversion rules:

- replace GLSL ES 1.00 `attribute` with vertex-stage `in`;
- replace `varying` with vertex `out` and fragment `in` using matching types;
- replace `gl_FragColor` with a declared fragment output;
- replace `texture2D` with `texture`;
- use `gl_FragCoord.xy` in standard fragment entry points;
- declare functions before use or add exact forward declarations;
- keep integer and floating-point expressions type-correct;
- treat a missing uniform location as possible compiler optimization, not always as initialization failure.

Shader source extraction must preserve `#version` at byte zero. Prefer dedicated source files or trim known surrounding whitespace before compilation.

## Compile And Link Diagnostics

Never discard shader logs:

```js
function compileShader(gl, type, source) {
  const shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    const log = gl.getShaderInfoLog(shader) || "Unknown shader compile failure";
    gl.deleteShader(shader);
    throw new Error(log);
  }
  return shader;
}
```

After attaching shaders, check `LINK_STATUS` and include `getProgramInfoLog()` in the thrown error. Validate attribute, uniform, framebuffer, and texture setup only after a successful link.

## Resolution And Timing

Keep drawing-buffer size synchronized with CSS size and device pixel ratio while capping pixel density when the effect is expensive:

```js
const dpr = Math.min(window.devicePixelRatio || 1, 2);
const width = Math.max(1, Math.floor(canvas.clientWidth * dpr));
const height = Math.max(1, Math.floor(canvas.clientHeight * dpr));
if (canvas.width !== width || canvas.height !== height) {
  canvas.width = width;
  canvas.height = height;
}
gl.viewport(0, 0, width, height);
```

Pass drawing-buffer dimensions to the shader. Use elapsed seconds from a monotonic clock, and clamp simulation delta time after tab suspension.

## Stable Sphere Tracing

For a conservative signed distance field `mapScene`, advance by the returned distance, stop near the surface, and cap both travel and iteration count:

```glsl
const int MAX_STEPS = 96;
const float MAX_DISTANCE = 60.0;

float march(vec3 origin, vec3 direction, out int steps) {
    float travel = 0.0;
    steps = 0;
    for (int i = 0; i < MAX_STEPS; ++i) {
        vec3 point = origin + direction * travel;
        float distanceToScene = mapScene(point);
        float epsilon = 0.0005 * max(1.0, travel);
        steps = i + 1;
        if (abs(distanceToScene) < epsilon) return travel;
        travel += max(distanceToScene * 0.8, epsilon);
        if (travel > MAX_DISTANCE) break;
    }
    return -1.0;
}
```

The `0.8` safety factor tolerates mildly non-conservative fields. It does not fix an invalid distance estimator; inspect field scaling after domain deformation. Do not use sphere tracing for participating media, where fixed or adaptive volume integration is the appropriate algorithm.

Estimate normals with a tetrahedral gradient to reduce field evaluations:

```glsl
vec3 sceneNormal(vec3 p, float travel) {
    float e = 0.0005 * max(1.0, travel);
    vec2 k = vec2(1.0, -1.0);
    return normalize(
        k.xyy * mapScene(p + k.xyy * e) +
        k.yyx * mapScene(p + k.yyx * e) +
        k.yxy * mapScene(p + k.yxy * e) +
        k.xxx * mapScene(p + k.xxx * e)
    );
}
```

Offset secondary rays along the normal to reduce self-intersection. Keep the offset proportional to the hit epsilon rather than using one scene-independent magic value.

## Multipass Rules

- Check framebuffer completeness after every attachment configuration.
- Never sample from the texture currently attached as the active draw target.
- Use two state textures and swap read/write roles after each pass.
- Match texture internal format, format, type, filtering, and extension support.
- Initialize state textures explicitly; uninitialized texels are not valid state.
- Keep simulation resolution independent from display resolution when possible.
- Use a fixed simulation step and a bounded number of catch-up steps.

For post-processing, render scene color to a texture, then draw a full-screen triangle into the default framebuffer. Apply tone mapping before transfer to display space; avoid applying gamma correction twice.

## Performance Budgets

Begin with conservative limits and raise them only after measurement:

- surface marching: 64 to 96 steps for interactive scenes;
- shadow marching: 16 to 32 steps;
- volume samples: 32 to 64 with front-to-back early termination;
- noise octaves: 4 to 6;
- device pixel ratio: cap at 1.5 or 2 for expensive full-screen effects.

Avoid hidden products of nested loops. A 96-step march with a 32-step shadow and six noise octaves can become thousands of evaluations per pixel. Use bounds, lower-resolution passes, level-of-detail, and early exits before micro-optimizing arithmetic.

## Visual Debugging

Temporarily replace final color with one diagnostic at a time:

| Signal | Output | Healthy result |
|---|---|---|
| UV | `vec3(uv * 0.5 + 0.5, 0.0)` | Smooth centered gradient |
| Normal | `normal * 0.5 + 0.5` | Smooth orientation colors |
| Depth | `vec3(travel / MAX_DISTANCE)` | Continuous distance bands |
| Step count | `vec3(float(steps) / float(MAX_STEPS))` | Hot areas only near detail |
| SDF sign | two contrasting colors | Stable zero crossing |
| Alpha | `vec3(alpha)` | Monotonic volume accumulation |

When the frame is blank:

1. Check context creation, compile log, link log, and framebuffer status.
2. Clear to a conspicuous color and draw the full-screen triangle without custom shading.
3. Verify viewport and resolution uniforms.
4. Replace the fragment output with a constant color.
5. Reintroduce coordinates, scene distance, normals, lighting, and post effects in that order.

## Shader and Host Integration Checks

- Shader compilation and program linking succeed with logs checked.
- Resize, high-density displays, tab suspension, and context loss are handled as required by the host application.
- No pass reads and writes the same texture.
- Loop bounds and render resolution stay within the measured frame budget.
- Diagnostic modes or focused tests cover math helpers where practical.
- The effect degrades cleanly when motion reduction or lower performance is required by the surrounding interface.

