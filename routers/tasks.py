from database.mongo_database import MongoDatabase
from database.model import Category
from typing import List
import geojson

from celery import shared_task

