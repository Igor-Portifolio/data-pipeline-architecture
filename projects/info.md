# General Structure

Each client must have a dedicated project structure.
Every project should contain its own pipeline and customized files tailored to that specific client.

Custom files created during analysis may later be promoted to the general project if they prove reusable. Until then, they must remain isolated.
These client-specific artifacts must be stored in the `extra/` folder.

When starting a new client project, the standard procedure is:

1. Copy the `projeto_geral` directory.
2. Rename it according to the new client or project name.
3. Customize pipelines and supporting files as needed.

The `projeto_geral` directory serves as the canonical template and must remain clean, stable, and reusable.
