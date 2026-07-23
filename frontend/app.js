document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate-btn');
    const startOverBtn = document.getElementById('start-over-btn');
    const copyBtn = document.getElementById('copy-btn');
    const notesInput = document.getElementById('notes-input');
    const errorMsg = document.getElementById('error-msg');
    
    const inputSection = document.getElementById('input-section');
    const loadingOverlay = document.getElementById('loading-overlay');
    const outputSection = document.getElementById('output-section');
    const proposalDoc = document.getElementById('proposal-doc');

    const proposalTitle = document.getElementById('proposal-title');
    const proposalDate = document.getElementById('proposal-date');
    const proposalSummary = document.getElementById('proposal-summary');
    const proposalDeliverables = document.getElementById('proposal-deliverables');
    const proposalTimeline = document.getElementById('proposal-timeline');
    const proposalHours = document.getElementById('proposal-hours');
    const proposalTotal = document.getElementById('proposal-total');

    // Input CTA state logic
    notesInput.addEventListener('input', () => {
        generateBtn.disabled = notesInput.value.trim().length === 0;
    });

    generateBtn.addEventListener('click', async () => {
        const notes = notesInput.value.trim();
        if (!notes) return;

        // UI Transition to Loading State
        errorMsg.classList.add('hidden');
        notesInput.disabled = true;
        generateBtn.disabled = true;
        inputSection.style.opacity = '0';
        inputSection.style.transform = 'scale(0.98)';
        
        setTimeout(() => {
            inputSection.classList.add('hidden');
            loadingOverlay.classList.remove('hidden');
        }, 300);

        try {
            const response = await fetch('http://127.0.0.1:8000/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ notes })
            });

            if (!response.ok) {
                throw new Error('Failed to generate proposal');
            }

            const data = await response.json();
            renderProposal(data);

            // UI Transition to Output State
            loadingOverlay.classList.add('hidden');
            outputSection.classList.remove('hidden');
            
            setTimeout(() => {
                proposalDoc.classList.add('animate-in');
            }, 50);

        } catch (err) {
            console.error(err);
            // Revert state on error
            loadingOverlay.classList.add('hidden');
            inputSection.classList.remove('hidden');
            setTimeout(() => {
                inputSection.style.opacity = '1';
                inputSection.style.transform = 'scale(1)';
            }, 50);
            notesInput.disabled = false;
            generateBtn.disabled = false;
            errorMsg.classList.remove('hidden');
        }
    });

    startOverBtn.addEventListener('click', () => {
        notesInput.value = '';
        notesInput.disabled = false;
        generateBtn.disabled = true;
        
        proposalDoc.classList.remove('animate-in');
        outputSection.classList.add('hidden');
        inputSection.classList.remove('hidden');
        setTimeout(() => {
            inputSection.style.opacity = '1';
            inputSection.style.transform = 'scale(1)';
        }, 50);
    });

    copyBtn.addEventListener('click', () => {
        // Build markdown proposal structure
        const titleText = `# ${proposalTitle.innerText}\nDate: ${proposalDate.innerText}\n\n`;
        const summaryText = `## Executive Summary\n${proposalSummary.innerText}\n\n`;
        
        const deliverablesListText = Array.from(proposalDeliverables.children)
            .map(li => `* ${li.innerText}`)
            .join('\n');
        const deliverablesText = `## Scope of Work & Deliverables\n${deliverablesListText}\n\n`;
        
        const timelineListText = Array.from(proposalTimeline.querySelectorAll('tr'))
            .map(tr => {
                const tds = tr.querySelectorAll('td');
                if (tds.length >= 2) {
                    return `* **${tds[0].innerText}**: ${tds[1].innerText}`;
                }
                return '';
            })
            .filter(Boolean)
            .join('\n');
        const timelineText = `## Timeline & Phases\n${timelineListText}\n\n`;
        
        const pricingText = `## Project Investment\n* Hourly Rate: $100/hr\n* Estimated Hours: ${proposalHours.innerText}\n* Total Estimated Investment: ${proposalTotal.innerText}`;

        const fullText = `${titleText}${summaryText}${deliverablesText}${timelineText}${pricingText}`;
        
        navigator.clipboard.writeText(fullText).then(() => {
            const originalText = copyBtn.innerText;
            copyBtn.innerText = 'Copied!';
            setTimeout(() => {
                copyBtn.innerText = originalText;
            }, 2000);
        });
    });

    function renderProposal(data) {
        proposalTitle.textContent = data.title || "Project Proposal";
        proposalDate.textContent = new Date().toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        
        proposalSummary.textContent = data.summary;
        
        // Deliverables
        proposalDeliverables.innerHTML = (data.deliverables || []).map(d => `<li>${d}</li>`).join('');
        
        // Timeline
        proposalTimeline.innerHTML = (data.timeline || []).map(t => `
            <tr>
                <td>${t.phase}</td>
                <td>${t.duration}</td>
            </tr>
        `).join('');
        
        // Pricing
        proposalHours.textContent = `${data.estimatedHours} hrs`;
        proposalTotal.textContent = `$${data.totalPrice.toLocaleString()}`;
    }
});
