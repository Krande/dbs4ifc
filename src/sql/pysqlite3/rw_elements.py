import sqlite3


def insert_polyline(conn, points):
    c = conn.cursor()

    c.execute("INSERT INTO IfcCurve DEFAULT VALUES")
    polyline_id = c.lastrowid
    c.execute("INSERT INTO IfcPolyline (ID) VALUES (?)", (polyline_id,))

    for point in points:
        c.execute("INSERT INTO IfcCartesianPoint (X, Y, Z) VALUES (?, ?, ?)", point)
        point_id = c.lastrowid
        c.execute(
            "INSERT INTO IfcPolylinePoints (PolylineID, PointID) VALUES (?, ?)",
            (polyline_id, point_id),
        )

    conn.commit()
    return polyline_id


def insert_arbitrary_closed_profile_def(conn, outer_curve_id):
    c = conn.cursor()

    c.execute("INSERT INTO IfcProfileDef (ProfileType) VALUES (?)", ("AREA",))
    profile_id = c.lastrowid
    c.execute(
        "INSERT INTO IfcArbitraryClosedProfileDef (ID, OuterCurve) VALUES (?, ?)",
        (profile_id, outer_curve_id),
    )

    conn.commit()
    return profile_id


def insert_sample_data(conn):
    c = conn.cursor()

    c.execute("INSERT INTO IfcCartesianPoint (X, Y, Z) VALUES (?, ?, ?)", (0, 0, 0))
    point_id = c.lastrowid

    c.execute("INSERT INTO IfcDirection (X, Y, Z) VALUES (?, ?, ?)", (0, 0, 1))
    direction_id = c.lastrowid

    c.execute("INSERT INTO IfcProfileDef (ProfileType) VALUES (?)", ("AREA",))
    profile_id = c.lastrowid

    polyline_points = [(0, 0, 0), (5, 0, 0), (5, 5, 0), (0, 5, 0), (0, 0, 0)]
    polyline_id = insert_polyline(conn, polyline_points)
    print(f"Inserted polyline with ID: {polyline_id}")

    profile_id = insert_arbitrary_closed_profile_def(conn, polyline_id)

    c.execute(
        "INSERT INTO IfcArbitraryClosedProfileDef (ID, OuterCurve) VALUES (?, ?)",
        (profile_id, 1),
    )

    c.execute(
        """INSERT INTO IfcExtrudedAreaSolid
                 (SweptArea, Position, ExtrudedDirection, Depth)
                 VALUES (?, ?, ?, ?)""",
        (profile_id, point_id, direction_id, 10),
    )
    extruded_id = c.lastrowid

    conn.commit()

    return extruded_id


def read_geometry(conn, extruded_id):
    c = conn.cursor()

    c.execute(
        """SELECT e.SweptArea, e.Position, e.ExtrudedDirection, e.Depth,
                        p.X, p.Y, p.Z, d.X, d.Y, d.Z
                 FROM IfcExtrudedAreaSolid AS e
                 JOIN IfcCartesianPoint AS p ON e.Position = p.ID
                 JOIN IfcDirection AS d ON e.ExtrudedDirection = d.ID
                 WHERE e.ID = ?""",
        (extruded_id,),
    )

    row = c.fetchone()
    if row:
        geometry = {
            "swept_area": row[0],
            "position": (row[4], row[5], row[6]),
            "extruded_direction": (row[7], row[8], row[9]),
            "depth": row[3],
        }
        return geometry
    else:
        return None


def main():
    db_file = "ifc_sqlite.db"
    conn = sqlite3.connect(db_file)
    # create_tables(conn)

    extruded_id = insert_sample_data(conn)
    print(f"Inserted sample geometry with ID: {extruded_id}")

    geometry = read_geometry(conn, extruded_id)
    print("Read geometry:", geometry)

    conn.close()


if __name__ == "__main__":
    main()
