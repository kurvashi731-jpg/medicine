// --- DONOR REGISTRATION LOGIC ---
const donorForm = document.getElementById("donorForm");
if (donorForm) {
donorForm.addEventListener("submit", async function(event) {
    event.preventDefault(); 

    const donorData = {
        name: document.getElementById("name").value,
        blood_group: document.getElementById("blood_group").value,
        phone_number: document.getElementById("phone_number").value,
        city: "Ranchi"
    };

    try {
        const response = await fetch("https://emergency-help-yb5a.onrender.com", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(donorData)
        });

        if (response.ok) {
            alert("Registration successful! Thank you for being a donor in Ranchi.");
            donorForm.reset(); 
        } else {
            const errorData = await response.json();
            alert("Registration failed: " + errorData.detail);
        }
    } catch (error) {
        console.error("Network Error:", error);
        alert("Could not connect to the MedLink server.");
    }
});
}

// --- PATIENT REGISTRATION LOGIC ---
const patientForm = document.getElementById("patientForm");
if (patientForm) {
patientForm.addEventListener("submit", async function(event) {
    event.preventDefault(); 

    // Make sure these match the IDs in patient.html
    const patientData = {
        name: document.getElementById("patient_name").value,
        age: parseInt(document.getElementById("patient_age").value),
        blood_group: document.getElementById("patient_blood_group").value,
        phone_number: document.getElementById("patient_phone").value,
        symptoms: document.getElementById("patient_symptoms").value,
        city: "Ranchi"
    };

    try {
        // Notice this points to /api/patients/ instead of donors
        const response = await fetch("https://emergency-help-yb5a.onrender.com", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(patientData)
        });

        if (response.ok) {
            alert("Patient request submitted successfully! Searching for donors...");
            patientForm.reset(); 
        } else {
            const errorData = await response.json();
            alert("Submission failed: " + errorData.detail);
        }
    } catch (error) {
        console.error("Network Error:", error);
        alert("Could not connect to the MedLink server.");
    }
});
}