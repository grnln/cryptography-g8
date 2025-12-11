document.addEventListener("DOMContentLoaded", function () {
    // COLUMN RESIZE
    const tables = document.querySelectorAll("table");
    tables.forEach(table => {
        const ths = table.querySelectorAll("th");
        ths.forEach(th => {
            const resizer = document.createElement("div");
            resizer.classList.add("resizer");
            th.appendChild(resizer);

            let startX, startWidth;
            resizer.addEventListener("mousedown", (e) => {
                startX = e.pageX;
                startWidth = th.offsetWidth;
                document.documentElement.style.cursor = "col-resize";

                function onMouseMove(e) {
                    const newWidth = startWidth + (e.pageX - startX);
                    th.style.width = newWidth + "px";
                }

                function onMouseUp() {
                    document.documentElement.style.cursor = "";
                    document.removeEventListener("mousemove", onMouseMove);
                    document.removeEventListener("mouseup", onMouseUp);
                }

                document.addEventListener("mousemove", onMouseMove);
                document.addEventListener("mouseup", onMouseUp);
            });
        });
    });

    // PAGINATION FUNCTION
    function makePaginate(tableId, rowsPerPage) {
        const table = document.getElementById(tableId);
        const tbody = table.querySelector("tbody");
        const rows = Array.from(tbody.querySelectorAll("tr"));
        const paginationDiv = document.getElementById(tableId + "_pagination");

        let currentPage = 1;
        const totalPages = Math.ceil(rows.length / rowsPerPage);

        function renderPage(page) {
            const start = (page - 1) * rowsPerPage;
            const end = start + rowsPerPage;
            rows.forEach((row, index) => {
                row.style.display = (index >= start && index < end) ? "" : "none";
            });
            // update buttons
            paginationDiv.querySelectorAll("button").forEach(btn => {
                btn.disabled = false;
            });
            if(page === 1) paginationDiv.querySelector(".prev").disabled = true;
            if(page === totalPages) paginationDiv.querySelector(".next").disabled = true;
        }

        // initial render
        renderPage(currentPage);

        // event listeners
        paginationDiv.querySelector(".prev").addEventListener("click", () => {
            if(currentPage > 1) { currentPage--; renderPage(currentPage); }
        });
        paginationDiv.querySelector(".next").addEventListener("click", () => {
            if(currentPage < totalPages) { currentPage++; renderPage(currentPage); }
        });
    }

    const tablesToPaginate = ["tp_table", "te_table", "ta_table", "merged_table"];
    tablesToPaginate.forEach(tableId => {
        if (document.getElementById(tableId)) {
            makePaginate(tableId, 10);
        }
    });
});
