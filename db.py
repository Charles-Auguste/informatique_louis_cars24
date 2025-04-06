import mysql.connector
from pydantic import BaseModel, EmailStr
from typing import Any, Tuple, Union
import os
import uuid
from enum import Enum
import pandas as pd
from dotenv import load_dotenv

load_dotenv()  # take environment variables


class FuelType(str, Enum):
    PETROL = "Petrol"
    DIESEL = "Diesel"
    CNG = "CNG"


class TransmissionType(str, Enum):
    MANUAL = "Manual"
    AUTOMATIC = "Automatic"


class RatingType(str, Enum):
    STAR_1 = "1 star"
    STAR_2 = "2 star"
    STAR_3 = "3 star"
    STAR_4 = "4 star"
    STAR_5 = "5 star"


# Database schemas
# ================


class Table(BaseModel):
    def __init__(self, **data):
        super().__init__(**data)
        name = self.__class__.__name__.lower()
        setattr(self, f"id_{name}", str(uuid.uuid4()))

    def get_values(self):
        return tuple(
            (
                self.model_dump().get(field, field.value)
                if isinstance(field, Enum)
                else field
            )
            for field in self.model_dump().values()
        )

    def get_keys(self):
        return tuple(self.model_dump().keys())


# Tables
class Engine(Table):
    id_engine: str = None
    fuel_type: FuelType
    capacity: float


class Transmission(Table):
    id_transmission: str = None
    transmission_type: TransmissionType


class Model(Table):
    id_model: str = None
    model_name: str
    manufacturing_year: int
    id_engine: str
    id_transmission: str


class Customer(Table):
    id_customer: str = None
    first_name: str
    last_name: str
    email: EmailStr
    rating: RatingType


class Transaction(Table):
    id_transaction: str = None
    id_customer: str
    id_model: str
    price: float
    km_driven: float
    spare_key: bool
    ownership: int
    imperfections: int
    repainted_parts: int


# Connector
class MySQLConnector(BaseModel):

    host: str = os.environ.get("host")
    user: str = os.environ.get("user")
    password: str = os.environ.get("password")
    database: str = os.environ.get("db_name")

    db: Any = None

    def connect(self):
        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )

    def add_entry(
        self,
        entry: Union[Engine, Transmission, Transaction, Customer, Model],
    ):
        assert self.db is not None, "No connection for database"
        cursor = self.db.cursor()
        # Check if table exist
        table_name = entry.__class__.__name__.lower()
        cursor.execute("SHOW TABLES")
        available_tables = []
        for x in cursor:
            available_tables.append(x[0])
        assert table_name in available_tables, "Table does not exist"

        keys = ", ".join([f"`{key}`" for key in entry.get_keys()])
        values = ", ".join(
            [
                f"'{value}'" if isinstance(value, str) else str(value)
                for value in entry.get_values()
            ]
        )

        sql = f"INSERT INTO {table_name} ({keys}) VALUES ({values})"

        cursor.execute(sql)
        self.db.commit()

        return getattr(entry, f"id_{table_name}")

    def execute(self, sql: str):
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(results, columns=columns)
        except Exception:
            print("Error while doing sql query")
            df = pd.DataFrame()
        return df
