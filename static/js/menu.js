document.addEventListener("DOMContentLoaded", () => {
    const menuItemFormModal = document.getElementById('menuItemFormModal');
    const formTitle = document.getElementById('formTitle');
    const menuItemForm = document.getElementById('menuItemForm');

    function showAddMenuItemForm() {
        formTitle.textContent = 'Add Menu Item';
        menuItemForm.itemId.value = '';
        menuItemForm.name.value = '';
        menuItemForm.category.value = '';
        menuItemForm.price.value = '';
        menuItemForm.description.value = '';
        menuItemForm.is_available.value = 'true';
        menuItemFormModal.hidden = false;
    }

    function showEditMenuItemForm(id) {
        const row = document.querySelector(`tr[data-id='${id}']`);
        if (!row) return;
        formTitle.textContent = 'Edit Menu Item';
        menuItemForm.itemId.value = id;
        menuItemForm.name.value = row.children[0].textContent.trim();
        menuItemForm.category.value = row.children[1].textContent.trim();
        menuItemForm.price.value = parseFloat(row.children[2].textContent.trim());
        menuItemForm.description.value = row.children[3].textContent.trim();;
        menuItemForm.is_available.value = (row.children[4].textContent.trim() === 'Yes').toString();
        menuItemFormModal.hidden = false;
    }

    function hideMenuItemForm() {
        menuItemFormModal.hidden = true;
    }

    async function submitMenuItemForm(event) {
        event.preventDefault();
        const id = menuItemForm.itemId.value;
        const data = {
            name: menuItemForm.name.value.trim(),
            category: menuItemForm.category.value.trim(),
            price: parseFloat(menuItemForm.price.value),
            description: menuItemForm.description.value.trim(),
            is_available: menuItemForm.is_available.value === 'true'
        };
        if (!data.name || data.price <= 0) {
            alert('Name and valid price are required.');
            return;
        }
        try {
            let url = '/menu/add';
            if (id) url = `/menu/edit/${id}`;
            const resp = await fetch(url, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            const result = await resp.json();
            showToast(result.message, result.status);
            if (result.status === 'success') location.reload();
        } catch {
            showToast('Failed to save menu item.', 'error');
        }
    }

    async function deleteMenuItem(id) {
        if (!confirm('Are you sure to delete this menu item?')) return;
        try {
            const resp = await fetch(`/menu/delete/${id}`, {method: 'POST'});
            const result = await resp.json();
            showToast(result.message, result.status);
            if (result.status === 'success') location.reload();
        } catch {
            showToast('Failed to delete menu item.', 'error');
        }
    }

    // ✅ Expose functions to window for use in onclick=""
    window.showAddMenuItemForm = showAddMenuItemForm;
    window.showEditMenuItemForm = showEditMenuItemForm;
    window.hideMenuItemForm = hideMenuItemForm;
    window.submitMenuItemForm = submitMenuItemForm;
    window.deleteMenuItem = deleteMenuItem;
});