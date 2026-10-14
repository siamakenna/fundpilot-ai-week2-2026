# Browser verification

The original application was opened at http://127.0.0.1:7860 after restarting its
local service. Browser connection refusals before the restart were genuine and
were not counted as successful UI tests.

Actual browser actions in reference mode (no AI):

| Profile | Opportunity | Observed result | Download link visible |
|---|---|---|---|
| Alex | Early Career | ELIGIBLE BASED ON SUPPLIED EVIDENCE | Yes |
| Alex | Graduate Student Only | NOT ELIGIBLE | Yes |
| Casey | Early Career | NEEDS VERIFICATION | Yes |

`starter-ui-unknown.png` and `starter-ui-unknown.txt` are authentic captures of the
third case. `final-ui-fixture-eligible.png` captures the redesigned three-step UI
and the explicit no-model label. Unit tests separately exercise all three UI
callbacks and verify the actual generated file content.

Native screen-recording tools are unavailable in this automation environment.
See `docs/LOCAL_CAPTURE_STEPS.md` for exact macOS recording instructions. Screenshots
are not claimed to be a video. No testimonial or first-user session was staged.

## Release live-mode check

Alex / Enrolled Graduate Student Mobility Grant was run through the actual browser
with **Live local Gemma** selected. The UI returned NOT ELIGIBLE, 1 MATCH, 2 NOT
MATCH, 0 UNKNOWN, and displayed 31.7 seconds. `live-ui-graduate.png` and
`live-ui-graduate.txt` record that result. The download link was clicked through
the browser; its actual downloaded file is preserved as
`live-ui-downloaded-report.md`. This extra UI request is not counted in the
six-case benchmark. Its two negative findings identify graduate enrollment and
the $600 request ceiling.
