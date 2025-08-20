async function addToPDF(id, type) {
    const form = document.getElementById("add-experience-form");
    const formData = new FormData(form);
    const response = await fetch(`${EDIT_PDF_URL}?type=${type}&object-id=${id}&action=add`, {
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
    const response = await fetch(`${EDIT_PDF_URL}?type=${type}&object-id=${id}&action=remove`, {
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


async function updateChangesItem(id, type, editedData) {
    const formData = new FormData(form);
    const response = await fetch(`${EDIT_URL}?type=${type}&object-id=${id}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": formData.get("csrfmiddlewaretoken")
        },
        body: JSON.stringify(editedData)
    });

    if (response.ok) {
        const data = await response.json();
        console.log("Item updated successfully:", data);
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
        console.error("Error updating item");
    }
}


async function editItem(id, type) {
    const experienceContent = document.getElementById(`experience-${id}`);

    const experienceName = experienceContent.querySelector('[data-field="name"]');
    const experienceOrganisation = experienceContent.querySelector('[data-field="organisation"]');
    const experienceDate = experienceContent.querySelector('[data-field="date"]');
    const experienceLocation = experienceContent.querySelector('[data-field="location"]');
    
    const descriptions = document.getElementById(`descriptions-${id}`)
    const experienceDescriptions = descriptions.getElementsByClassName("description");

    const descriptionsTuple = Array.from(experienceDescriptions).map((desc) => {
        const descText = desc.innerText;
        const descId = desc.dataset.id;
        return [descId, descText];
    });
    
    const editedData = {
        name: experienceName.innerText,
        organisation: experienceOrganisation.innerText,
        date: experienceDate.innerText,
        location: experienceLocation.innerText,
        descriptions: descriptionsTuple,
    };

    updateChangesItem(id, type, editedData)
}
