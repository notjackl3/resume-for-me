async function addToPDF(id, type) {
    const form = document.getElementById("add-experience-form");
    const formData = new FormData(form);
    const response = await fetch(`${EDIT_URL}?type=${type}&object-id=${id}&action=add`, {
        method: "PATCH",
        headers: {
            "X-CSRFToken": formData.get("csrfmiddlewaretoken")
        },
    });

    if (response.ok) {
        const data = await response.json();
        console.log("Item deleted successfully:", data);
        fetch(RESET_PANEL_URL);
        const formData2 = new FormData(form);
        await fetch(PREPARE_PDF_URL, {
            method: "POST",
            headers: {
                "X-CSRFToken": formData2.get("csrfmiddlewaretoken")
            },
            body: formData2
        })
    } else {
        console.error("Error adding item to PDF");
    }
}

async function removeFromPDF(id, type) {
    const form = document.getElementById("add-experience-form");
    const formData = new FormData(form);
    const response = await fetch(`${EDIT_URL}?type=${type}&object-id=${id}&action=remove`, {
        method: "PATCH",
        headers: {
            "X-CSRFToken": formData.get("csrfmiddlewaretoken")
        },
    });

    if (response.ok) {
        const data = await response.json();
        console.log("Item deleted successfully:", data);
        fetch(RESET_PANEL_URL);
        const formData2 = new FormData(form);
        await fetch(PREPARE_PDF_URL, {
            method: "POST",
            headers: {
                "X-CSRFToken": formData2.get("csrfmiddlewaretoken")
            },
            body: formData2
        })
    } else {
        console.error("Error removing item from PDF");
    }
}

async function deleteItem(id, type) {
    const formData = new FormData(form);
    const response = await fetch(`${DELETE_URL}?type=${type}&object-id=${id}`, {
        method: "DELETE",
        headers: {
            "X-CSRFToken": formData.get("csrfmiddlewaretoken")
        },
    });

    if (response.ok) {
        const data = await response.json();
        console.log("Item deleted successfully:", data);
        fetch(RESET_PANEL_URL);
        const formData2 = new FormData(form);
        await fetch(PREPARE_PDF_URL, {
            method: "POST",
            headers: {
                "X-CSRFToken": formData2.get("csrfmiddlewaretoken")
            },
            body: formData2
        })
    } else {
        console.error("Error deleting item");
    }
}