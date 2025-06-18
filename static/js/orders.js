const orderDetailsModal = document.getElementById('orderDetailsModal');
const orderDetailsTableBody = document.querySelector('#orderDetailsTable tbody');
const orderFormModal = document.getElementById('orderFormModal');
const orderForm = document.getElementById('orderForm');

function showOrderDetails(orderId) {
    if (!orderDetailsModal || !orderDetailsTableBody) return;
    orderDetailsTableBody.innerHTML = '<tr><td colspan="3" style="text-align:center;">Loading...</td></tr>';
    orderDetailsModal.classList.remove('hidden');

    fetch(`/orders/${orderId}/items`)
        .then(resp => resp.json())
        .then(items => {
            if (!items.length) {
                orderDetailsTableBody.innerHTML = '<tr><td colspan="3" style="text-align:center;">No items found.</td></tr>';
                return;
            }
            orderDetailsTableBody.innerHTML = items.map(item => `
                <tr>
                    <td>${item.name}</td>
                    <td>${item.quantity}</td>
                    <td>$${parseFloat(item.price).toFixed(2)}</td>
                </tr>
            `).join('');
        })
        .catch(() => {
            orderDetailsTableBody.innerHTML = '<tr><td colspan="3" style="text-align:center; color:red;">Failed to load order items.</td></tr>';
        });
}

function hideOrderDetails() {
    if (orderDetailsModal) {
        orderDetailsModal.classList.add('hidden');
    }
}

function showAddOrderForm() {
    if (!orderForm || !orderFormModal) return;
    orderForm.reset();
    document.querySelectorAll('input[name="menu_item_ids"]').forEach(chk => {
        document.getElementById('qty-' + chk.value).disabled = true;
        document.getElementById('qty-' + chk.value).value = 1;
    });
    orderFormModal.hidden = false;
}

function hideOrderForm() {
    if (orderFormModal) {
        orderFormModal.hidden = true;
    }
}

document.querySelectorAll('input[name="menu_item_ids"]').forEach(chk => {
    chk.addEventListener('change', function () {
        const qtyInput = document.getElementById('qty-' + this.value);
        qtyInput.disabled = !this.checked;
        if (!this.checked) qtyInput.value = 1;
    });
});

function capitalizeStatus(status) {
  return status.charAt(0).toUpperCase() + status.slice(1);
}

function handleStatusChange(selectEl, orderId) {
  const newStatus = selectEl.value;
  const oldStatus = selectEl.getAttribute('data-current');
  if (newStatus === oldStatus) {
    // Prevent duplicate update
    return;
  }
  changeOrderStatus(orderId, newStatus);
}

function getStatusBadgeClass(status) {
  switch (status) {
    case 'pending': return 'badge badge-warning';
    case 'preparing': return 'badge badge-info';
    case 'served': return 'badge badge-success';
    case 'paid': return 'badge badge-primary';
    case 'cancelled': return 'badge badge-danger';
    default: return 'badge badge-secondary';
  }
}

async function loadOrders() {
    const tbody = document.querySelector('#ordersTable tbody');
    if (!tbody) return;

    try {
        const resp = await fetch('/orders/list');
        if (!resp.ok) throw new Error("Failed to load");
        const orders = await resp.json();
        tbody.innerHTML = '';

        if (orders.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7">No orders found.</td></tr>';
            return;
        }

        orders.forEach(order => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${order.id}</td>
                <td>${order.table_name || 'N/A'}</td>
                <td>${order.user_name || 'N/A'}</td>
                <td><span class="${getStatusBadgeClass(order.status)}">${capitalizeStatus(order.status)}</span></td>
                <td>${parseFloat(order.total).toFixed(2)}</td>
                <td>${order.created_at_str || 'N/A'}</td>
                <td style="display: flex;">
                    <select data-current="${order.status}" onchange="handleStatusChange(this, ${order.id})">
                        ${['pending', 'preparing', 'served', 'paid', 'cancelled'].map(status =>
                        `<option value="${status}" ${status === order.status ? 'selected' : ''}>${capitalizeStatus(status)}</option>`
                        ).join('')}
                    </select>
                    <button onclick="showOrderDetails(${order.id})" title="View Details">
                        <span class="material-icons">info</span>
                    </button>
                    <button onclick="deleteOrder(${order.id})" title="Delete Order">
                        <span class="material-icons">delete</span>
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (err) {
        console.error(err);
        showToast("Failed to refresh orders", "error");
    }
}

async function updateItemTotal(itemId, price) {
    const checkbox = document.querySelector(`#menu-item-${itemId}`);
    const qtyInput = document.querySelector(`#qty-${itemId}`);
    const totalSpan = document.querySelector(`#total-${itemId}`);

    let quantity = parseInt(qtyInput.value) || 0;
    let total = 0;

    if (checkbox.checked && quantity > 0) {
        total = price * quantity;
    }

    totalSpan.textContent = `₹${total.toFixed(2)}`;
    updateGrandTotal();
}

async function updateGrandTotal() {
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

    document.getElementById('grandTotal').textContent = `₹${grandTotal.toFixed(2)}`;
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('input[name="menu_item_ids"]').forEach(cb => {
        const itemId = cb.value;
        const qtyInput = document.getElementById(`qty-${itemId}`);
        const row = cb.closest('tr');
        const priceText = row?.querySelectorAll('td')[3]?.innerText?.replace('₹', '').trim();
        const price = parseFloat(priceText) || 0;

        // Initial state
        qtyInput.disabled = !cb.checked;

        cb.addEventListener('change', () => {
            qtyInput.disabled = !cb.checked;
            if (!cb.checked) qtyInput.value = 1;
            updateItemTotal(itemId, price);
        });

        qtyInput.addEventListener('input', () => {
            updateItemTotal(itemId, price);
        });
    });
});

async function changeOrderStatus(orderId, newStatus) {
    try {
        const resp = await fetch(`/orders/${orderId}/status`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: newStatus })
        });
        const result = await resp.json();
        showToast(result.message, result.status);
        if (result.status === "success") {
            loadOrders();  // Refresh the table
        }
    } catch (err) {
        console.error(err);
        showToast("Failed to update status.", "error");
    }
}

async function resetOrderForm() {
    // Reset all checkbox selections
    orderForm.reset();

    // Disable and reset all quantity inputs
    orderForm.querySelectorAll('input[type="number"]').forEach(input => {
        input.disabled = true;
        input.value = 1;
    });

    // Reset item total display
    document.querySelectorAll('span[id^="total-"]').forEach(span => {
        span.textContent = '₹0.00';
    });

    // Reset grand total
    const grandTotalSpan = document.getElementById('grandTotal');
    if (grandTotalSpan) grandTotalSpan.textContent = '₹0.00';
}

async function submitOrderForm(event) {
    event.preventDefault();
    const tableId = orderForm.table_id.value;
    if (!tableId) {
        alert('Please select a table.');
        return;
    }

    let items = [];
    document.querySelectorAll('input[name="menu_item_ids"]:checked').forEach(chk => {
        const qtyInput = document.getElementById('qty-' + chk.value);
        let qty = parseInt(qtyInput.value);
        if (qty <= 0 || isNaN(qty)) qty = 1;
        items.push({ menu_item_id: parseInt(chk.value), quantity: qty });
    });

    if (!items.length) {
        alert('Please select at least one menu item.');
        return;
    }

    try {
        const resp = await fetch('/orders/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ table_id: parseInt(tableId), items: items })
        });
        const result = await resp.json();
        if (result.status === 'success') {
            showToast('Order added successfully! Thank you.', 'success');
            resetOrderForm(); 
            hideOrderForm();
            loadOrders();
        } else {
            showToast('Failed to add order: ' + result.message, 'error');
        }
    } catch {
        showToast('Failed to add order.', 'error');
    }
}

async function deleteOrder(id) {
    if (!confirm('Are you sure to delete this order?')) return;
    try {
        const resp = await fetch(`/orders/delete/${id}`, { method: 'POST' });
        const result = await resp.json();
        showToast(result.message, result.status);
        if (result.status === 'success') loadOrders();
    } catch {
        showToast('Failed to delete order.', 'error');
    }
}
