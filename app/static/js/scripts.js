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

    async function fetchData(prompt, endpoint) {
        try {
            const response = await fetchWithTimeout(endpoint, {
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
            // Fetch raw response and update the DOM
            const rawResult = await fetchData(prompt, "/get_raw_response");

            if (rawResult.success) {
                const resultHTML1 = `<h3>Modality: Raw</h3><h5 class="text-lightgrey">Company: ${prompt}</h5><pre>${rawResult.response}</pre>`;
                displayResult(resultModel1, resultHTML1);
            } else {
                displayError(resultModel1, rawResult.error);
            }

            // Fetch engineered response and update the DOM
            const engineeredResult = await fetchData(prompt, "/get_engineered_response");

            if (engineeredResult.success) {
                const resultHTML2 = `<h3>Modality: Engineered</h3><h5 class="text-lightgrey">Company: ${prompt}</h5><pre>${engineeredResult.response}</pre>`;
                displayResult(resultModel2, resultHTML2);
            } else {
                displayError(resultModel2, engineeredResult.error);
            }
        } catch (error) {
            displayError(resultModel1, "An error occurred while processing the request. Please try again later.");
            displayError(resultModel2, "An error occurred while processing the request. Please try again later.");
        }
        
        toggleSpinner(false);
    }

    function displayResult(resultModel, resultHTML) {
        resultModel.innerHTML = resultHTML;
    }
    
    function displayError(resultModel, message) {
        resultModel.innerHTML = `<p class="text-danger">${message}</p>`;
    }

    promptForm.addEventListener('submit', handleFormSubmit);
});

