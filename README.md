# gs-docs

Unified documentation for projects

# Objetive

Read all my repositories, gets mkdocs metadata and build a integrated documentation.

## .gsdoc file

The `.gsdoc` file will be found in the root of each repository, with some metadata used to build the documentation.

```yaml .gsdoc
doc_folder: "docs"  # 
enabled: true
project_title: "Name of the project"
project_description: "Description of the project"
```

## Configuration

The configuration of the tool can be read from a yaml file or from environment variables.

### ORGANIZATIONS

List of organizations (comma separated) from within will be get all repositories. 

* Environment: `GSDOCS_ORGS` 
* Configuration: `organizations`

### USERS

List of user (comma separated) from within will be get all repositories.

* Environment: `GSDOCS_USERS`
* Configuration: `users`


### Configuration file

```yaml
organizations: 
  - escoteirando

users:
  - guionardo
```



