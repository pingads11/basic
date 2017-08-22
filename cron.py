from subprocess import STDOUT, check_output

"""
Here Cron timings are
                    minute=m
                    hour=h
                    day_of_month=dom
                    month=moy
                    day_of_week=dow 
"""

def cron_edit(cron_name, cron_file, job, m="*", h="*", dom="*", moy="*", dow="*", new_cron=False):
    cron_command = "{} {} {} {} {} {}".format(m, h, dom, moy, dow, job)

    try:
        output = []
        if new_cron:
            name_cmd = "echo '#{}' >> {}".format(cron_name, cron_file)
            output = check_output([name_cmd], stderr=STDOUT, shell=True)
            insert_cmd = "echo '{}' >> {}".format(cron_command, cron_file)
            output = check_output([insert_cmd], stderr=STDOUT, shell=True)
        else:
            sed_cmd = "sed -i '/{}/!b;n;c{}' {}".format(cron_name, cron_command, cron_file)
            output = check_output([sed_cmd], stderr=STDOUT, shell=True)
        for data in output:
            print (data)
        print "Cron deployed"
    except Exception as err:
        print str(err)


if __name__ == "__main__":
    name = "GTA"
    file = "/root/PycharmProjects/python3/cron.test"
    # if JOB is not provided then it will remove the cron
    job = "admin /usr/bin/python /var/home/root/result.py > /tmp/early_daily_result.log 2>&1"
    # if New Cron is not provide then it edit older one
    cron_edit(cron_name=name, cron_file=file, job=job, dom="11", new_cron=True)
