# TODO:
- Refactor structure of the project in modules

For each module:
    - Create models
    - -> Test model in pytest  
    -  create repositories
    -  create services
    -  create pydantic schemas
    -  create endpoints in routes
    -  create docs 
    
# Decisions:
-- Project should be divided in modules with a a core module for central configurations
-- Every module should respect the current structure models, repositories, services, schemas, routes


# Questions:
1. Should I create a new db testing, if so containers or local
-- containers, easy to set up and test but need new container infra
**-- local, a bit less flexible but can reuse what we have

2. What is the best way to test models?





