$compose_file = "docker-compose.yml"

docker-compose up --build --exit-code-from voronoi

$STATUS = $LastExitCode

docker-compose down --remove-orphans

if ($STATUS -eq 0)
{
    echo "tests passed"
}
else
{
    echo "tests failed"
}

exit $STATUS
