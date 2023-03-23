from django.shortcuts import render,redirect
from datetime import datetime,timedelta
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count,Sum,Case,When,F,Q
from .serializers import *
# from .apr_views import *
import pandas as pd
import xlwt
import json
from django.conf import settings