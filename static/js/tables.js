document.addEventListener("DOMContentLoaded", () => {
    const tableFormModal = document.getElementById('tableFormModal');
    const tableFormTitle = document.getElementById('tableFormTitle');
    const tableForm = document.getElementById('tableForm');

    function showAddTableForm() {
        tableFormTitle.textContent = 'Add New Table';
        tableForm.tableId.value = '';
        tableForm.name.value = '';
        tableForm.capacity.value = '';
        tableFormModal.hidden = false;
    }

    function showEditTableForm(id) {
        const row = document.querySelector(`tr[data-id='${id}']`);
        if (!row) return;
        tableFormTitle.textContent = 'Edit Table';
        tableForm.tableId.value = id;
        tableForm.name.value = row.children[0].textContent.trim();
        tableForm.capacity.value = row.children[1].textContent.trim();
        tableFormModal.hidden = false;
    }

    function hideTableForm() {
        tableFormModal.hidden = true;
    }

    async function submitTableForm(event) {
        event.preventDefault();
        const id = tableForm.tableId.value;
        const data = {
            name: tableForm.name.value.trim(),
            capacity: parseInt(tableForm.capacity.value)
        };
        if (!data.name || data.capacity <= 0) {
            alert('Table name and valid capacity are required.');
            return;
        }
        try {
            let url = '/tables/add';
            if (id) url = `/tables/edit/${id}`;
            const resp = await fetch(url, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            const result = await resp.json();
            showToast(result.message, result.status);
            if (result.status === 'success') location.reload();
        } catch {
            showToast('Failed to save table.', 'error');
        }
    }

    async function deleteTable(id) {
        if (!confirm('Are you sure to delete this table?')) return;
        try {
            const resp = await fetch(`/tables/delete/${id}`, {method: 'POST'});
            const result = await resp.json();
            showToast(result.message, result.status);
            if (result.status === 'success') location.reload();
        } catch {
            showToast('Failed to delete table.', 'error');
        }
    }
    
    // ✅ Expose functions to window for use in onclick=""
    window.showAddTableForm = showAddTableForm;
    window.showEditTableForm = showEditTableForm;
    window.hideTableForm = hideTableForm;
    window.submitTableForm = submitTableForm;
    window.deleteTable = deleteTable;
});