import sqlite3


def create_tables(conn):
    c = conn.cursor()

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS IfcCartesianPoint (
            ID INTEGER PRIMARY KEY,
            X REAL NOT NULL,
            Y REAL NOT NULL,
            Z REAL NOT NULL
        );
    """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS IfcDirection (
            ID INTEGER PRIMARY KEY,
            X REAL NOT NULL,
            Y REAL NOT NULL,
            Z REAL NOT NULL
        );
    """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS IfcExtrudedAreaSolid (
            ID INTEGER PRIMARY KEY,
            SweptArea INTEGER NOT NULL,
            Position INTEGER NOT NULL,
            ExtrudedDirection INTEGER NOT NULL,
            Depth REAL NOT NULL,
            FOREIGN KEY (SweptArea) REFERENCES IfcProfileDef(ID),
            FOREIGN KEY (Position) REFERENCES IfcCartesianPoint(ID),
            FOREIGN KEY (ExtrudedDirection) REFERENCES IfcDirection(ID)
        );
    """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS IfcProfileDef (
            ID INTEGER PRIMARY KEY,
            ProfileType TEXT NOT NULL,
            ProfileName TEXT
        );
    """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS IfcArbitraryClosedProfileDef (
            ID INTEGER PRIMARY KEY,
            OuterCurve INTEGER NOT NULL,
            FOREIGN KEY (ID) REFERENCES IfcProfileDef(ID),
            FOREIGN KEY (OuterCurve) REFERENCES IfcCurve(ID)
        );
    """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS IfcCurve (
            ID INTEGER PRIMARY KEY
        );
    """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS IfcPolyline (
            ID INTEGER PRIMARY KEY,
            FOREIGN KEY (ID) REFERENCES IfcCurve(ID)
        );
    """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS IfcPolylinePoints (
            PolylineID INTEGER NOT NULL,
            PointID INTEGER NOT NULL,
            PRIMARY KEY (PolylineID, PointID),
            FOREIGN KEY (PolylineID) REFERENCES IfcPolyline(ID),
            FOREIGN KEY (PointID) REFERENCES IfcCartesianPoint(ID)
        );
    """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS IfcRectangleProfileDef (
            ID INTEGER PRIMARY KEY,
            XDim REAL NOT NULL,
            YDim REAL NOT NULL,
            FOREIGN KEY (ID) REFERENCES IfcProfileDef(ID)
        );
    """
    )

    conn.commit()


def main():
    db_file = "ifc_sqlite.db"
    conn = sqlite3.connect(db_file)
    create_tables(conn)
    conn.close()


if __name__ == "__main__":
    main()
