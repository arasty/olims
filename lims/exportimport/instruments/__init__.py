import sys
import inspect

from dependencies.dependency import xml
from agilent.masshunter import quantitative
from dependencies.dependency import fiastar
from dependencies.dependency import auto
from dependencies.dependency import ft120
from dependencies.dependency import Ts9861x
from dependencies.dependency import xt20
from dependencies.dependency import go
from dependencies.dependency import axios_xrf
from alere.pima import beads, cd4
from lifetechnologies.qubit import qubit
from biodrop.ulite import ulite
from dependencies.dependency import tima
from sysmex.xs import i500, i1000
from beckmancoulter.access import model2
from dependencies.dependency import model48
from sealanalytical.aq2 import aq2
from dependencies.dependency import icp
from abaxis.vetscan import vs2
from scilvet.abc import plus
from dependencies.dependency import cs2000
from dependencies.dependency import wxrf

__all__ = ['abaxis.vetscan.vs2',
           'agilent.masshunter.quantitative',
           'alere.pima.beads',
           'alere.pima.cd4',
           'beckmancoulter.access.model2',
           'biodrop.ulite.ulite',
           'eltra.cs.cs2000',
           'foss.fiastar.fiastar',
           'foss.winescan.auto',
           'foss.winescan.ft120',
           'generic.xml',
           'horiba.jobinyvon.icp',
           'rigaku.supermini.wxrf',
           'rochecobas.taqman.model48',
           'thermoscientific.arena.xt20',
           'thermoscientific.gallery.Ts9861x',
           'panalytical.omnia.axios_xrf',
           'lifetechnologies.qubit.qubit',
           'sysmex.xs.i500',
           'sysmex.xs.i1000',
           'scilvet.abc.plus',
           'sealanalytical.aq2.aq2',
           'tescan.tima.tima',
           'thermoscientific.multiskan.go',
           ]


def getExim(exim_id):
    currmodule = sys.modules[__name__]
    members = [obj for name, obj in inspect.getmembers(currmodule) \
               if hasattr(obj, '__name__') \
               and obj.__name__.endswith(exim_id)]

    return members[0]
