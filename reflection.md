# Module 14 Reflection - FastAPI User Calculations

In Module 14, I implemented a complete FastAPI application that includes user registration/login and
BREAD operations for calculations. This helped me connect multiple concepts from earlier modules into
a single, testable service. I gained a clearer understanding of how routers, schemas, models,
and a database session work together in a production-style structure.

One of the biggest learning points was aligning my implementation with automated tests.
The integration tests reinforced the importance of consistent response formats, correct status codes,
and predictable behavior across the API. I also learned how small mismatches between schemas and models
can break the application at runtime, which encouraged me to validate my design carefully.

The Playwright E2E portion was especially valuable. It required me to ensure the static UI pages
used stable selectors (`data-testid`) and displayed clear success/error messages.
This highlighted the relationship between front-end validation and backend error handling.
It also reminded me that good UX is testable when the UI is designed with clarity and consistency.

Finally, setting up CI and Docker strengthened my DevOps workflow. Automating tests through GitHub Actions
and preparing the project for container deployment gave me more confidence in building applications that are
reproducible and easy to deploy. Overall, this module improved my ability to deliver a full-stack,
test-driven FastAPI project with a clean structure and reliable automation.
