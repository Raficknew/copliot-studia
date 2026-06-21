// Subscribe form handler
document.getElementById('subscribe-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const emailInput = document.getElementById('email-input');
    const email = emailInput.value.trim();
    const messageDiv = document.getElementById('message');
    
    try {
        const response = await fetch('/api/subscribe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email }),
        });
        
        const data = await response.json();
        
        if (data.success) {
            messageDiv.className = 'success';
            messageDiv.textContent = data.message;
            emailInput.value = '';
            
            // Reload page to update subscriber list
            setTimeout(() => location.reload(), 1500);
        } else {
            messageDiv.className = 'error';
            messageDiv.textContent = data.message;
        }
    } catch (error) {
        messageDiv.className = 'error';
        messageDiv.textContent = 'Failed to subscribe. Please try again.';
    }
});

// Unsubscribe button handlers
document.querySelectorAll('.unsubscribe-btn').forEach(button => {
    button.addEventListener('click', async (e) => {
        const email = e.target.dataset.email;
        
        if (!confirm(`Unsubscribe ${email}?`)) {
            return;
        }
        
        try {
            const response = await fetch('/api/unsubscribe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email }),
            });
            
            const data = await response.json();
            
            if (data.success) {
                location.reload();
            } else {
                alert(data.message);
            }
        } catch (error) {
            alert('Failed to unsubscribe. Please try again.');
        }
    });
});

// Send email form handler
document.getElementById('send-email-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const subjectInput = document.getElementById('subject-input');
    const bodyInput = document.getElementById('body-input');
    const htmlCheckbox = document.getElementById('html-checkbox');
    const messageDiv = document.getElementById('send-message');
    
    const subject = subjectInput.value.trim();
    const body = bodyInput.value.trim();
    const html = htmlCheckbox.checked;
    
    try {
        messageDiv.className = '';
        messageDiv.textContent = 'Sending emails...';
        messageDiv.style.display = 'block';
        
        const response = await fetch('/api/send-email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ subject, body, html }),
        });
        
        const data = await response.json();
        
        if (data.success) {
            messageDiv.className = 'success';
            messageDiv.textContent = data.message;
            subjectInput.value = '';
            bodyInput.value = '';
            htmlCheckbox.checked = false;
        } else {
            messageDiv.className = 'error';
            messageDiv.textContent = data.message;
        }
    } catch (error) {
        messageDiv.className = 'error';
        messageDiv.textContent = 'Failed to send emails. Please try again.';
    }
});
