async function applyCustomization() {
    const userPrompt = document.getElementById("userPrompt").value;

    try {
        const response = await fetch("http://localhost:5001/generate-styles", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ userPrompt })
        });

        const data = await response.json();
        if (data.error) throw new Error(data.error);

        const styles = data.styles;

        // Apply styles to chat box
        const chatBox = document.querySelector('.chat-box');
        if (chatBox) {
            if (styles['.chat-box']) {
                Object.entries(styles['.chat-box']).forEach(([property, value]) => {
                    chatBox.style[property] = value;
                });
            } else {
                // Reset to default if no styles are returned
                chatBox.style.border = "1px solid #ccc";
                chatBox.style.boxShadow = "0 4px 10px rgba(0, 0, 0, 0.1)";
            }
        }

        // Apply styles to chat input
        const chatInput = document.querySelector('.chat-input');
        if (chatInput && styles.chatInput) {
            Object.entries(styles.chatInput).forEach(([property, value]) => {
                chatInput.style[property] = value;
            });
        }

        // Apply styles to body
        if (styles.body) {
            Object.entries(styles.body).forEach(([property, value]) => {
                document.body.style[property] = value;
            });
        }

        // Apply styles to header h1
        const headerH1 = document.querySelector('.header h1');
        if (headerH1 && styles['.header h1']) {
            Object.entries(styles['.header h1']).forEach(([property, value]) => {
                headerH1.style[property] = value;
            });
        }

        // Apply border color to buttons
        const buttons = document.querySelectorAll('.example-prompt, .send-button, .reset-button');
        buttons.forEach(button => {
            if (styles['.button']) {
                Object.entries(styles['.button']).forEach(([property, value]) => {
                    button.style[property] = value;
                });
            }
            // Explicitly handle border and box-shadow
            if (styles['.button']?.border) {
                button.style.border = styles['.button'].border;
            }
            if (styles['.button']?.boxShadow) {
                button.style.boxShadow = styles['.button'].boxShadow;
            }
        });

        console.log("Styles applied successfully:", styles);
    } catch (error) {
        console.error("Error customizing UI:", error);
    }
}

function applyExamplePrompt(prompt) {
    const userPromptInput = document.getElementById("userPrompt");
    userPromptInput.value = prompt;

    const sendButton = document.querySelector('.send-button');
    if (sendButton) {
        sendButton.click();
    }
}

function resetStyles() {
    location.reload();
}