# envbuilder
Build an env file (.env) from python project

## Key capabilities

1. Create an .env file by scanning provided python project (full path) and save it under same project
2. Append a new env variables if .env already exists in project
3. Manual skip allowed on project scanning process

## Requirements
1. Python

## Scan a project and make/append .env

` envreqs [<project-full-path>]`

```
$ envreqs 'E:\Projects\py-sample-project'
```

## Skip the directory while scan and make .env

` envreqs <options> [<project-full-path>]`

```
$ envreqs --ignore ignore_dir /home/projects/sample_project/
```