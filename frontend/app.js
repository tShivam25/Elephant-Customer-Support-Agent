document.addEventListener('DOMContentLoaded', () => {
    const customerList = document.getElementById('customer-list');
    const chatMessages = document.getElementById('chat-messages');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const memoryToggle = document.getElementById('memory-toggle');
    const themeToggle = document.getElementById('theme-toggle');
    const demoBtn = document.getElementById('demo-btn');
    const quickReplies = document.getElementById('quick-replies');
    
    let currentCustomer = null;
    let customers = [];

    // Theme Toggle
    themeToggle.addEventListener('click', () => {
        const html = document.documentElement;
        if (html.getAttribute('data-theme') === 'dark') {
            html.setAttribute('data-theme', 'light');
            themeToggle.textContent = '☾';
        } else {
            html.setAttribute('data-theme', 'dark');
            themeToggle.textContent = '☀';
        }
    });

    // Tab Switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            e.target.classList.add('active');
            document.getElementById(`tab-${e.target.dataset.tab}`).classList.add('active');
        });
    });

    // Load Customers
    fetch('/api/customers')
        .then(res => res.json())
        .then(data => {
            customers = data;
            renderCustomerList();
        });

    function renderCustomerList() {
        customerList.innerHTML = '';
        customers.forEach(cust => {
            const div = document.createElement('div');
            div.className = 'customer-item';
            div.innerHTML = `<h4>${cust.name}</h4><p>${cust.company}</p>`;
            div.addEventListener('click', () => selectCustomer(cust, div));
            customerList.appendChild(div);
        });
    }

    function selectCustomer(cust, element) {
        document.querySelectorAll('.customer-item').forEach(el => el.classList.remove('active'));
        if(element) element.classList.add('active');
        
        currentCustomer = cust;
        document.getElementById('current-customer-name').textContent = cust.name;
        document.getElementById('current-customer-plan').textContent = cust.plan;
        
        // Update Profile Tab
        document.getElementById('profile-card').innerHTML = `
            <strong>${cust.name}</strong><br>
            🏢 ${cust.company}<br>
            💻 ${cust.environment}<br>
            📞 ${cust.preference}<br>
            😠 Tone: ${cust.tone}
        `;
        
        chatMessages.innerHTML = `<div class="empty-state">
            <div class="glow-circle"></div>
            <h2>Chat with ${cust.name}</h2>
            <p>Start a new conversation.</p>
        </div>`;
        
        clearBrain();
    }

    function clearBrain() {
        document.getElementById('memories-used-list').innerHTML = '';
        document.getElementById('facts-stored-list').innerHTML = '';
        document.getElementById('tools-used-list').innerHTML = '';
        document.getElementById('decision-summary').textContent = '-';
    }

    function addMessage(text, sender) {
        // Remove empty state if present
        const emptyState = chatMessages.querySelector('.empty-state');
        if (emptyState) emptyState.remove();

        const msg = document.createElement('div');
        msg.className = `message ${sender}`;
        msg.textContent = text;
        chatMessages.appendChild(msg);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return msg;
    }

    function showTyping() {
        const emptyState = chatMessages.querySelector('.empty-state');
        if (emptyState) emptyState.remove();

        const div = document.createElement('div');
        div.className = 'typing-indicator';
        div.id = 'typing';
        div.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function removeTyping() {
        const el = document.getElementById('typing');
        if(el) el.remove();
    }

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = chatInput.value.trim();
        if(!text || !currentCustomer) return;
        
        chatInput.value = '';
        addMessage(text, 'user');
        showTyping();
        
        const useMemory = memoryToggle.checked;
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    customer_id: currentCustomer.id,
                    message: text,
                    use_memory: useMemory
                })
            });
            const data = await response.json();
            
            removeTyping();
            
            // Handle reply with basic streaming effect
            const msgEl = addMessage('', 'agent');
            let i = 0;
            function typeChar() {
                if(i < data.reply.length) {
                    msgEl.textContent += data.reply.charAt(i);
                    i++;
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                    setTimeout(typeChar, 10);
                }
            }
            typeChar();

            // Update Brain Panel
            updateBrain(data);

        } catch (err) {
            removeTyping();
            addMessage("Sorry, I encountered an error.", 'agent');
        }
    });

    function updateBrain(data) {
        document.getElementById('decision-summary').textContent = data.decision_summary || '-';
        
        const memList = document.getElementById('memories-used-list');
        memList.innerHTML = '';
        if(data.memories && data.memories.length > 0) {
            data.memories.forEach(m => {
                const card = document.createElement('div');
                card.className = 'card memory-card';
                card.textContent = m;
                memList.appendChild(card);
            });
        } else {
            memList.innerHTML = '<p class="text-muted">None used.</p>';
        }

        const toolsList = document.getElementById('tools-used-list');
        toolsList.innerHTML = '';
        if(data.tools && data.tools.length > 0) {
            data.tools.forEach(t => {
                const item = document.createElement('div');
                item.className = 'tool-item';
                item.innerHTML = `<strong>${t.name}</strong><br><small>${JSON.stringify(t.args)}</small>`;
                toolsList.appendChild(item);
            });
        } else {
            toolsList.innerHTML = '<p class="text-muted">None used.</p>';
        }

        const factsList = document.getElementById('facts-stored-list');
        factsList.innerHTML = '';
        if(data.facts_stored && data.facts_stored.length > 0) {
            data.facts_stored.forEach(f => {
                const card = document.createElement('div');
                card.className = 'card memory-card';
                card.textContent = "✅ " + f;
                factsList.appendChild(card);
            });
        } else {
            factsList.innerHTML = '<p class="text-muted">None stored.</p>';
        }
    }

    // Quick Replies
    quickReplies.addEventListener('click', (e) => {
        if(e.target.classList.contains('chip')) {
            chatInput.value = e.target.textContent;
            chatForm.dispatchEvent(new Event('submit'));
        }
    });

    // Demo Button (Priya Nair scenario)
    demoBtn.addEventListener('click', () => {
        const priya = customers.find(c => c.id === 'hero_priya');
        if(priya) {
            // Find and click the element
            const items = document.querySelectorAll('.customer-item');
            items.forEach(el => {
                if(el.querySelector('h4').textContent === priya.name) {
                    el.click();
                }
            });
            setTimeout(() => {
                chatInput.value = "My invoice sync is failing again. I need this fixed immediately.";
                chatForm.dispatchEvent(new Event('submit'));
            }, 500);
        }
    });
});
