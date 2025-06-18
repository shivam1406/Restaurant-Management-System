// Function to calculate item total and grand total
function updateItemTotal(itemId, price) {
    const checkbox = document.getElementById(`menu-item-${itemId}`);
    const qtyInput = document.getElementById(`qty-${itemId}`);
    const totalSpan = document.getElementById(`total-${itemId}`);

    let quantity = parseInt(qtyInput.value) || 0;
    let total = 0;

    if (checkbox.checked && quantity > 0) {
        total = price * quantity;
    }

    totalSpan.textContent = `₹${total.toFixed(2)}`;
    updateGrandTotal();
}

function updateGrandTotal() {
    let grandTotal = 0;
    const rows = document.querySelectorAll('#menuItemsContainer tr');

    rows.forEach(row => {
        const checkbox = row.querySelector('input[type="checkbox"]');
        const qtyInput = row.querySelector('input[type="number"]');
        const priceText = row.querySelectorAll('td')[3]?.innerText?.replace('₹', '')?.trim();
        const price = parseFloat(priceText) || 0;
        const quantity = parseInt(qtyInput?.value) || 0;

        if (checkbox?.checked && quantity > 0) {
            grandTotal += price * quantity;
        }
    });

    const grandTotalEl = document.getElementById('grandTotal');
    if (grandTotalEl) {
        grandTotalEl.textContent = `₹${grandTotal.toFixed(2)}`;
    }
}

// ✅ Attach quantity toggle logic after DOM is ready
document.addEventListener("DOMContentLoaded", () => {
    const menuItemsContainer = document.getElementById('menuItemsContainer');

    if (!menuItemsContainer) return;

    menuItemsContainer.querySelectorAll('input[type="checkbox"]').forEach(chk => {
        chk.addEventListener('change', () => {
            const qtyInput = document.getElementById('qty-' + chk.value);
            qtyInput.disabled = !chk.checked;
            if (!chk.checked) qtyInput.value = 1;

            const priceCell = chk.closest('tr').querySelectorAll('td')[3];
            const price = parseFloat(priceCell.textContent.replace('₹', '').trim()) || 0;
            updateItemTotal(chk.value, price);
        });
    });

    menuItemsContainer.querySelectorAll('input[type="number"]').forEach(input => {
        input.addEventListener('input', () => {
            const row = input.closest('tr');
            const checkbox = row.querySelector('input[type="checkbox"]');
            const id = checkbox.value;
            const priceText = row.querySelectorAll('td')[3].innerText.replace('₹', '');
            const price = parseFloat(priceText) || 0;
            updateItemTotal(id, price);
        });
    });
});

// ✅ Handle form submission manually
async function submitGuestOrderForm(event) {
    event.preventDefault();

    const guestOrderForm = document.getElementById('guestOrderForm');
    const menuItemsContainer = document.getElementById('menuItemsContainer');
    const submitBtn = document.getElementById('submitBtn');
    const tableId = document.getElementById('tableSelect').value;

    if (!tableId) {
        alert('Please select a table.');
        return;
    }

    let items = [];
    menuItemsContainer.querySelectorAll('input[type="checkbox"]:checked').forEach(chk => {
        const qtyInput = document.getElementById('qty-' + chk.value);
        let quantity = parseInt(qtyInput.value);
        if (isNaN(quantity) || quantity < 1) quantity = 1;
        items.push({ menu_item_id: parseInt(chk.value), quantity });
    });

    if (!items.length) {
        alert('Please select at least one menu item.');
        return;
    }

    submitBtn.disabled = true;

    try {
        const response = await fetch('/public/order', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ table_id: parseInt(tableId), items: items })
        });

        const result = await response.json();
        if (result.status === 'success') {
            showToast('Order placed successfully! Thank you.', 'success');
            guestOrderForm.reset();
            menuItemsContainer.querySelectorAll('input[type="number"]').forEach(input => {
                input.disabled = true;
                input.value = 1;
            });
            document.getElementById('grandTotal').textContent = '₹0.00';
            document.querySelectorAll('span[id^="total-"]').forEach(span => span.textContent = '₹0.00');
        } else {
            showToast('Failed to place order: ' + result.message, 'error');
        }
    } catch {
        showToast('Error placing order.', 'error');
    } finally {
        submitBtn.disabled = false;
    }
}