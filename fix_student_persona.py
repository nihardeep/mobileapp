import re

with open('app.js', 'r') as f:
    js = f.read()

old_logic = """        if (isStudentPersonaActive) {
            wrapper.classList.add('active');
            const header = document.getElementById("homeHeaderSection");
            if (header) header.style.paddingTop = "8px";
            triggerHaptic('medium', 'Student Persona On');
        } else {
            wrapper.classList.remove('active');
            const header = document.getElementById("homeHeaderSection");
            if (header) header.style.paddingTop = "40px";
            triggerHaptic('light', 'Student Persona Off');
        }
    }
}"""

new_logic = """        if (isStudentPersonaActive) {
            wrapper.classList.add('active');
            const header = document.getElementById("homeHeaderSection");
            if (header) header.style.paddingTop = "8px";
            triggerHaptic('medium', 'Student Persona On');
            
            // Apply Student Discount to Passenger Screen Fare
            const totalFare = document.getElementById('passenger-total-fare');
            const origFare = document.getElementById('passenger-original-fare');
            const studentBadge = document.getElementById('passenger-student-badge');
            if (totalFare && origFare && studentBadge) {
                totalFare.innerText = '₹ 5,564'; // 10% off 6182
                totalFare.style.color = 'var(--indigo-blue)';
                origFare.style.display = 'block';
                studentBadge.style.display = 'block';
            }
        } else {
            wrapper.classList.remove('active');
            const header = document.getElementById("homeHeaderSection");
            if (header) header.style.paddingTop = "40px";
            triggerHaptic('light', 'Student Persona Off');
            
            // Remove Student Discount from Passenger Screen Fare
            const totalFare = document.getElementById('passenger-total-fare');
            const origFare = document.getElementById('passenger-original-fare');
            const studentBadge = document.getElementById('passenger-student-badge');
            if (totalFare && origFare && studentBadge) {
                totalFare.innerText = '₹ 6,182';
                totalFare.style.color = '#0f172a';
                origFare.style.display = 'none';
                studentBadge.style.display = 'none';
            }
        }
    }
}"""

js = js.replace(old_logic, new_logic)

with open('app.js', 'w') as f:
    f.write(js)
