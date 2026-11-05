import json
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent


def main():
    with duckdb.connect() as db:
        db.execute((ROOT / "cube.sql").read_text(encoding="utf-8"))
        columns = "month, region, category, orders, revenue_cents, units"
        cube = db.execute(f"select {columns} from cube order by 1, 2, 3").fetchall()
        total = db.execute("select count(*), sum(revenue_cents), sum(units) from sales").fetchone()
        assert len(cube) == 144
        assert tuple(sum(row[index] for row in cube) for index in (3, 4, 5)) == total
        for key in range(3):
            dimension = columns.split(", ")[key]
            expected = db.execute(
                f"select {dimension}, count(*), sum(revenue_cents), sum(units) "
                f"from sales group by {dimension} order by 1"
            ).fetchall()
            for label, *values in expected:
                subset = [row for row in cube if row[key] == label]
                assert [sum(row[index] for row in subset) for index in (3, 4, 5)] == values
    payload = json.dumps(cube, ensure_ascii=False)
    site = ROOT / "site"
    site.mkdir(exist_ok=True)
    template = (ROOT / "index.html").read_text(encoding="utf-8")
    (site / "index.html").write_text(template.replace("__CUBE__", payload), encoding="utf-8")
    print(f"Cubo verificado: {len(cube)} celdas, {total[0]} pedidos, {total[2]} unidades.")


if __name__ == "__main__":
    main()
