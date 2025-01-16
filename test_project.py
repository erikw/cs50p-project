import project
from project import get_sem_version


def test_get_sem_version():
    PROG_SEM_VERSION = (1, 0, 0)
    assert "1.0.0" == get_sem_version()

    project.PROG_SEM_VERSION = (2, 3, 4)
    assert "2.3.4" == get_sem_version()
