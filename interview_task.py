JOB_RUNTIME = 1
JOB_COOLDOWN = 5


# 1. Define lower_i is important for algorithm complexity
# 2. Nice to have: use enumerate() in first loop
# 3. Nice to have: use find() / rfind()
def calculate_total_runtime_original(jobs):
    result = len(jobs)*JOB_RUNTIME
    for i in range(len(jobs)):
        if jobs[i] in jobs[0:i]:
            yet = i - [j for j, e in enumerate(jobs[0:i]) if e == jobs[i]][-1]-1
            result += JOB_COOLDOWN - yet*JOB_RUNTIME
    return result


def calculate_total_runtime_1(jobs):
    result = len(jobs)*JOB_RUNTIME

    for i, job in enumerate(jobs):
        lower_i = i - JOB_COOLDOWN if i >= JOB_COOLDOWN else 0
        previous_jobs = jobs[lower_i:i]
        previous_job_index = jobs.find(job, lower_i, i)

        coincidences = [j for j, e in enumerate(jobs[lower_i:i]) if e == jobs[i]]
        try:
            last_coincidence = coincidences[-1]
        except IndexError:
            continue
        else:
            result += JOB_COOLDOWN - ((i - last_coincidence - 1) * JOB_RUNTIME)

    return result


def calculate_total_runtime(jobs):
    result = len(jobs) * JOB_RUNTIME

    for i, job in enumerate(jobs):
        lower_i = i - JOB_COOLDOWN if i >= JOB_COOLDOWN else 0
        last_coincidence = jobs.rfind(job, lower_i, i)

        if last_coincidence == -1:
            continue

        result += JOB_COOLDOWN - ((i - last_coincidence - 1) * JOB_RUNTIME)

    return result


if __name__ == '__main__':
    assert calculate_total_runtime('AAA') == 13
    assert calculate_total_runtime('ABC') == 3
    assert calculate_total_runtime('ABCDA') == 7
    assert calculate_total_runtime('AA') == 7

    # assert calculate_total_runtime('AAA')
    # assert calculate_total_runtime('ABC')
    # assert calculate_total_runtime('ABCDA')
    # assert calculate_total_runtime('ABCDAEFG')
    # assert calculate_total_runtime('ABCDAABCDA')
    # assert calculate_total_runtime('AA')
    # assert calculate_total_runtime('ABCDEFGA')

    print('All tests pass')
