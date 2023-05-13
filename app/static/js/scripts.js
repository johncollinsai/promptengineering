document.addEventListener('DOMContentLoaded', function () {
    const promptForm = document.getElementById('prompt-form');
    const resultModel1 = document.getElementById('result-model-1');
    const resultModel2 = document.getElementById('result-model-2');
    const spinner = document.querySelector('.spinner');
    const skeletonScreen = document.getElementById('skeleton-screen');

    function toggleSpinner(visible) {
        spinner.style.display = visible ? 'flex' : 'none';
        skeletonScreen.classList.toggle('d-none', !visible);
    }

    function fetchWithTimeout(resource, options, timeout = 60000) {
        return Promise.race([
            fetch(resource, options),
            new Promise((_, reject) =>
                setTimeout(() => reject(new Error("Request timed out")), timeout)
            ),
        ]);
    }

    async function fetchData(prompt) {
        try {
            const response = await fetchWithTimeout("/get_completion", {
                method: "POST",
                body: new FormData(promptForm),
            }, 180000); // Set the timeout to 3 minutes (180000 milliseconds)
        
            if (response.ok) {
                const data = await response.json();
                return data;
            } else {
                return { success: false, error: "An error occurred while fetching data. Please try again later." };
            }
        } catch (error) {
            return {
                success: false,
                error: "An error occurred while fetching data. Please try again later.",
            };
        }
    }
    
    async function handleFormSubmit(event) {
        event.preventDefault();
        toggleSpinner(true);
        
        const prompt = promptForm.elements["prompt"].value;
        
        try {
            const result = await fetchData(prompt);
    
            if (result.success) {
                const resultHTML1 = `<h3>Modality: Raw</h3><h5 class="text-lightgrey">Company: ${prompt}</h5><pre>${result.response.raw}</pre>`;
                const resultHTML2 = `<h3>Modality: Engineered</h3><h5 class="text-lightgrey">Company: ${prompt}</h5><pre>${result.response.engineered}</pre>`;
                displayResult(resultHTML1, resultHTML2);
            } else {
                displayError(result.error);
            }
        } catch (error) {
            displayError("An error occurred while processing the request. Please try again later.");
        }
        
        toggleSpinner(false);
    }

    function displayResult(result1, result2) {
        resultModel1.innerHTML = result1;
        resultModel2.innerHTML = result2;
    }
    
    function displayError(message) {
        resultModel1.innerHTML = `<p class="text-danger">${message}</p>`;
        resultModel2.innerHTML = `<p class="text-danger">${message}</p>`;
    }

    promptForm.addEventListener('submit', handleFormSubmit);
});
