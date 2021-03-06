#
# Short script populates the database with some test/example data
#
#
import os
import django
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'analytics_automated_project.settings.dev')

django.setup()


from django.core.files.uploadedfile import SimpleUploadedFile

from analytics_automated.models import Backend, Job, Task, Step
from analytics_automated.models import Parameter, Submission, Result



def populate():
    # clear out everything
    Backend.objects.all().delete()
    Job.objects.all().delete()
    Task.objects.all().delete()
    Step.objects.all().delete()
    Submission.objects.all().delete()
    Parameter.objects.all().delete()

    this_backend = add_backend(name="local1",
                               server_type=Backend.LOCALHOST,
                               ip="127.0.0.1",
                               port=80,
                               root_path="/tmp/")
    this_task = add_task(backend=this_backend,
                         name="task1",
                         in_glob=".in",
                         out_glob=".out",
                         executable="/usr/bin/ls")
    that_task = add_task(backend=this_backend,
                         name="task2",
                         in_glob=".out",
                         out_glob=".final",
                         executable="/usr/bin/rm")
    this_param = add_parameter(task=this_task,
                               flag="-lah",
                               default=None,
                               bool_valued=True,
                               rest_alias="all")
    that_param = add_parameter(task=that_task,
                               flag="-a",
                               default=10,
                               bool_valued=False,
                               rest_alias="number")

    this_job = add_job(name="job1",
                       runnable=True)

    add_step(this_job, this_task, 0)
    add_step(this_job, that_task, 1)

    file1 = SimpleUploadedFile('file1.txt',
                               bytes('these are the file contents!', 'utf-8'))
    file2 = SimpleUploadedFile('file2.txt',
                               bytes('these are the file contents!', 'utf-8'))
    id1 = str(uuid.uuid1())
    id2 = str(uuid.uuid1())
    add_submisson(this_job, "sub1", id1,
                  "a@b.com", "127.0.0.1", file1)
    add_submisson(this_job, "sub2", id2,
                  "a@b.com", "127.0.0.1", file2)

    for b in Backend.objects.all():
        for t in Task.objects.filter(backend=b):
            print("- {0} - {1}".format(str(b), str(t)))


def add_backend(name, server_type, ip, port, root_path):
    print("Hello")
    b = Backend.objects.create(name=name)
    b.server_type = server_type
    b.ip = ip
    b.port = port
    b.root_path = root_path
    b.save()
    return b


def add_task(backend, name, in_glob, out_glob, executable):
    t = Task.objects.create(backend=backend)
    t.name = name
    t.in_glob = in_glob
    t.out_glob = out_glob
    t.executable = executable
    t.save()
    return t


def add_parameter(task, flag, default, bool_valued, rest_alias):
    p = Parameter.objects.create(task=task)
    p.flag = flag
    p.default = default
    p.bool_valued = bool_valued
    p.rest_alias = rest_alias
    p.save()
    return p


def add_job(name, runnable):
    j = Job.objects.create(name=name)
    j.runnable = True
    j.save()
    return j


def add_step(job, task, ordering):
    s = Step.objects.create(job=job, task=task, ordering=ordering)
    s.save()
    return s


def add_submisson(job, name, UUID, email, ip, input_data):
    s = Submission.objects.create(job=job)
    s.submission_name = name
    s.UUID = UUID
    s.email = email
    s.ip = ip
    s.input_data = input_data
    s.save()
    return(s)

# Start execution here!
if __name__ == '__main__':
    print("Starting A_A population script...")
    populate()
