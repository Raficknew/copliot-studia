// API helper function
async function apiRequest(url, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        },
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(url, options);
        const result = await response.json();
        return { success: response.ok, data: result, status: response.status };
    } catch (error) {
        return { success: false, data: { error: 'Network error' }, status: 0 };
    }
}

// Show message helper
function showMessage(elementId, message, isSuccess) {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.className = `message ${isSuccess ? 'success' : 'error'} show`;
    
    setTimeout(() => {
        element.classList.remove('show');
    }, 5000);
}

// Load subscribers
async function loadSubscribers() {
    const result = await apiRequest('/api/subscribers');
    
    const countElement = document.getElementById('subscriberCount');
    const listElement = document.getElementById('subscriberList');
    
    if (result.success) {
        const subscribers = result.data.subscribers;
        countElement.textContent = `Total Subscribers: ${subscribers.length}`;
        
        if (subscribers.length === 0) {
            listElement.innerHTML = '<li style="text-align: center; color: #999;">No subscribers yet</li>';
        } else {
            listElement.innerHTML = subscribers
                .map(email => `<li>${email}</li>`)
                .join('');
        }
    } else {
        countElement.textContent = 'Error loading subscribers';
        listElement.innerHTML = '<li style="text-align: center; color: #e74c3c;">Failed to load</li>';
    }
}

// Subscribe form handler
document.getElementById('subscribeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const emailInput = document.getElementById('subscribeEmail');
    const email = emailInput.value.trim();
    
    const button = e.target.querySelector('button');
    button.disabled = true;
    button.textContent = 'Subscribing...';
    
    const result = await apiRequest('/api/subscribe', 'POST', { email });
    
    if (result.success) {
        showMessage('subscribeMessage', result.data.message, true);
        emailInput.value = '';
        loadSubscribers();
    } else {
        showMessage('subscribeMessage', result.data.error || 'Subscription failed', false);
    }
    
    button.disabled = false;
    button.textContent = 'Subscribe';
});

// Unsubscribe form handler
document.getElementById('unsubscribeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const emailInput = document.getElementById('unsubscribeEmail');
    const email = emailInput.value.trim();
    
    const button = e.target.querySelector('button');
    button.disabled = true;
    button.textContent = 'Unsubscribing...';
    
    const result = await apiRequest('/api/unsubscribe', 'POST', { email });
    
    if (result.success) {
        showMessage('unsubscribeMessage', result.data.message, true);
        emailInput.value = '';
        loadSubscribers();
    } else {
        showMessage('unsubscribeMessage', result.data.error || 'Unsubscribe failed', false);
    }
    
    button.disabled = false;
    button.textContent = 'Unsubscribe';
});

// Send email form handler
document.getElementById('sendEmailForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const subject = document.getElementById('emailSubject').value.trim();
    const body = document.getElementById('emailBody').value.trim();
    const html = document.getElementById('emailHtml').checked;
    
    const button = e.target.querySelector('button');
    button.disabled = true;
    button.textContent = 'Sending...';
    
    const result = await apiRequest('/api/send-email', 'POST', {
        subject,
        body,
        html
    });
    
    if (result.success) {
        showMessage('sendMessage', result.data.message, true);
        document.getElementById('emailSubject').value = '';
        document.getElementById('emailBody').value = '';
        document.getElementById('emailHtml').checked = false;
    } else {
        showMessage('sendMessage', result.data.error || 'Failed to send email', false);
    }
    
    button.disabled = false;
    button.textContent = 'Send Email';
});

// Refresh button handler
document.getElementById('refreshBtn').addEventListener('click', () => {
    loadSubscribers();
});

// Load subscribers on page load
document.addEventListener('DOMContentLoaded', () => {
    loadSubscribers();
});
