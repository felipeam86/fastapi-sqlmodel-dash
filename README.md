## Setting up postgres and populating with fake data

Launch a postgress instance with docker-compose and then populate with fake data
using the following two commands:

```bash
docker-compose up -d
python -m project.faker
```

Afterwards, you should have a db at the following address:
`postgresql://root:root@localhost:5432/sales`

### Stop and erase data
If you want to start from scratch, stop containers and remove volumes with:

```bash
docker-compose down -v
```
