#!/bin/bash
echo 'Testing API'

echo 'TASK 1'
printf '\nTest 1/5 week 01/09/2020 - 08/09/2020\n'

curl -s --location --request GET 'http://127.0.0.1:5000/task1/?week=01/09/2020%2012:00%20-%2008/09/2020%2012:00&sensor_id=TEK10'

printf '\nTest 2/5 week 08/09/2020 - 15/09/2020\n'

curl -s --location --request GET 'http://127.0.0.1:5000/task1/?week=08/09/2020%2012:00%20-%2015/09/2020%2012:00&sensor_id=TEK10'

printf '\nTest 3/5 week 15/09/2020 - 21/09/2020\n'

curl -s --location --request GET 'http://127.0.0.1:5000/task1/?week=15/09/2020%2012:00%20-%2021/09/2020%2012:00&sensor_id=TEK10'

printf '\n\nTest 4/5 wrong sensor_id\n'

curl -s --location --request GET 'http://127.0.0.1:5000/task1/?week=08/09/2020%2012:00%20-%2015/09/2020%2012:00&sensor_id=TEK100'

printf '\n\nTest 5/5 wrong week format (removed time)\n'

curl -s --location --request GET 'http://127.0.0.1:5000/task1/?week=03/09/2020%20%20-%2021/08/2020%2012:00&sensor_id=TEK100'

printf '\n\nTASK 2'

printf '\n\nTest 1/4 period 10/09/2020 - 12/09/2020\n'

curl -s --location --request GET 'http://127.0.0.1:5000/task2/?week=10/09/2020%2012:00%20-%2012/09/2020%2012:00&sensor_id=TEK10'

printf '\n\nTest 2/4 period 20/09/2020 - 25/09/2020\n'

curl -s --location --request GET 'http://127.0.0.1:5000/task2/?week=20/09/2020%2012:00%20-%2025/09/2020%2012:00&sensor_id=TEK10'

printf '\n\nTest 3/4 wrong sensorid (changed from TEK10 to KLM10)\n'

curl -s --location --request GET 'http://127.0.0.1:5000/task2/?week=20/09/2020%2012:00%20-%2025/09/2020%2012:00&sensor_id=KLM10'

printf '\n\nTest 4/4 period 20/09/2020 - 25/09/2020 and sensor_id = FFMM10\n'

curl -s --location --request GET 'http://127.0.0.1:5000/task2/?week=20/09/2020%2012:00%20-%2025/09/2020%2012:00&sensor_id=FFMM10'

printf '\n\nTASK 3'
printf '\n\nTest 1/3 machine_id = DEC1\n'

curl -s --location --request GET 'http://127.0.0.1:5000/task3/?machine_id=DEC1'

printf '\n\nTest 2/3 machine_id = BMM\n'

curl -s --location --request GET 'http://127.0.0.1:5000/task3/?machine_id=BMM'

printf '\n\nTest 3/3 machine_id = KLM00 (wrong machine id)\n'

curl -s --location --request GET 'http://127.0.0.1:5000/task3/?machine_id=KLM00'

$SHELL