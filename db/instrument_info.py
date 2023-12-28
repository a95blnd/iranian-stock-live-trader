import sqlite3
import json


class InstrumentInfoModel:
    def __init__(self, instrumentId, status, lVal18AFC, lVal30, cGrValCot, qPasCotFxeVal, qQtTranMarVal, qTitMinSaiOmProd, qTitMaxSaiOmProd, baseVol, insCode, zTitad, ipo, yVal, yDeComp, cSecVal, cSoSecVal, cComVal, flow, marketType, cIsin, cSocCSAC, id, lRfintAdfMsg, cFon, op, initialMargin, maintenanceMargin, requiredMargin, strikePrice, cSize, sDate, eDate, csDate, psDate, maxCOP, maxCAOP, maxBOP, maxMOP, maxOrders, uacIsin, cefo, baseInstrumentId, createdDateTime, modifiedDateTime):
        self.create_table()

        self.instrumentId = instrumentId
        self.status = status
        self.lVal18AFC = lVal18AFC
        self.lVal30 = lVal30
        self.cGrValCot = cGrValCot
        self.qPasCotFxeVal = qPasCotFxeVal
        self.qQtTranMarVal = qQtTranMarVal
        self.qTitMinSaiOmProd = qTitMinSaiOmProd
        self.qTitMaxSaiOmProd = qTitMaxSaiOmProd
        self.baseVol = baseVol
        self.insCode = insCode
        self.zTitad = zTitad
        self.ipo = ipo
        self.yVal = yVal
        self.yDeComp = yDeComp
        self.cSecVal = cSecVal
        self.cSoSecVal = cSoSecVal
        self.cComVal = cComVal
        self.flow = flow
        self.marketType = marketType
        self.cIsin = cIsin
        self.cSocCSAC = cSocCSAC
        self.id = id
        self.lRfintAdfMsg = lRfintAdfMsg
        self.cFon = cFon
        self.op = op
        self.initialMargin = initialMargin
        self.maintenanceMargin = maintenanceMargin
        self.requiredMargin = requiredMargin
        self.strikePrice = strikePrice
        self.cSize = cSize
        self.sDate = sDate
        self.eDate = eDate
        self.csDate = csDate
        self.psDate = psDate
        self.maxCOP = maxCOP
        self.maxCAOP = maxCAOP
        self.maxBOP = maxBOP
        self.maxMOP = maxMOP
        self.maxOrders = maxOrders
        self.uacIsin = uacIsin
        self.cefo = cefo
        self.baseInstrumentId = baseInstrumentId
        self.createdDateTime = createdDateTime
        self.modifiedDateTime = modifiedDateTime

    @staticmethod
    def _connect():
        conn = sqlite3.connect('instruments.db')
        cursor = conn.cursor()
        return conn, cursor

    @staticmethod
    def _close(conn):
        conn.commit()
        conn.close()

    @classmethod
    def create_table(cls):
        conn, cursor = cls._connect()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS instruments (
                instrumentId TEXT PRIMARY KEY,
                status TEXT,
                lVal18AFC TEXT,
                lVal30 TEXT,
                cGrValCot TEXT,
                qPasCotFxeVal REAL,
                qQtTranMarVal INTEGER,
                qTitMinSaiOmProd INTEGER,
                qTitMaxSaiOmProd INTEGER,
                baseVol INTEGER,
                insCode TEXT,
                zTitad INTEGER,
                ipo INTEGER,
                yVal INTEGER,
                yDeComp INTEGER,
                cSecVal TEXT,
                cSoSecVal TEXT,
                cComVal TEXT,
                flow TEXT,
                marketType TEXT,
                cIsin TEXT,
                cSocCSAC TEXT,
                id INTEGER,
                lRfintAdfMsg TEXT,
                cFon TEXT,
                op INTEGER,
                initialMargin INTEGER,
                maintenanceMargin INTEGER,
                requiredMargin INTEGER,
                strikePrice INTEGER,
                cSize INTEGER,
                sDate TEXT,
                eDate TEXT,
                csDate TEXT,
                psDate TEXT,
                maxCOP INTEGER,
                maxCAOP INTEGER,
                maxBOP INTEGER,
                maxMOP INTEGER,
                maxOrders INTEGER,
                uacIsin TEXT,
                cefo INTEGER,
                baseInstrumentId TEXT,
                createdDateTime TEXT,
                modifiedDateTime TEXT
            )
        ''')
        cls._close(conn)

    def save(self):
        conn, cursor = self._connect()
        fields = [key for key in self.__dict__ if not key.startswith('_')]
        values = [getattr(self, field) for field in fields]
        placeholders = ','.join(['?'] * len(fields))
        insert_query = f'INSERT INTO instruments ({",".join(fields)}) VALUES ({placeholders});'
        cursor.execute(insert_query, values)
        self._close(conn)

    @classmethod
    def get_all_instruments(cls):
        conn, cursor = cls._connect()
        cursor.execute('SELECT * FROM instruments')
        instrument_data = cursor.fetchall()
        cls._close(conn)
        if instrument_data:
            return [cls(*data) for data in instrument_data]
        return []

    @classmethod
    def get_instrument_by_id(cls, instrument_id):
        conn, cursor = cls._connect()
        cursor.execute('SELECT * FROM instruments WHERE instrumentId = ?', (instrument_id,))
        instrument_data = cursor.fetchone()
        cls._close(conn)
        if instrument_data:
            return cls(*instrument_data)
        return None

    def update(self):
        conn, cursor = self._connect()
        fields = [f'{key} = ?' for key in self.__dict__ if not key.startswith('_') and key != 'instrumentId']
        values = [getattr(self, field) for field in self.__dict__ if not field.startswith('_') and field != 'instrumentId']
        values.append(self.instrumentId)
        update_query = f'UPDATE instruments SET {",".join(fields)} WHERE instrumentId = ?;'
        cursor.execute(update_query, values)
        self._close(conn)

    @classmethod
    def delete_all_instruments(cls):
        conn, cursor = cls._connect()
        cursor.execute('DELETE FROM instruments')
        cls._close(conn)

    def delete(self):
        conn, cursor = self._connect()
        cursor.execute('DELETE FROM instruments WHERE instrumentId = ?', (self.instrumentId,))
        self._close(conn)
