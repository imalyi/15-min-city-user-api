import logging
from fastapi import Depends
from fastapi import APIRouter
from database.report_model import MongoDatabase
from database.get_database import get_database
from fastapi import FastAPI, HTTPException
from database.model import AddressIn, AddressOut
from typing import List
from database.model import Category
from database.es import fuzzy_search
import os
from database.heatmap_model import HeatMapModel

router = APIRouter()


@router.get("/")
async def generate_heatmap(categories: list[Category], database: MongoDatabase = Depends(get_database)):
    h = HeatMapModel()
    return h.generate(categories)
