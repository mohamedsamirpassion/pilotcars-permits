/**
 * Complete Load Planning JavaScript Implementation
 * ================================================
 * 
 * This file contains all the JavaScript logic needed for the Load Planning feature.
 * Include this file along with state_regulations.js for full functionality.
 * 
 * Features:
 * - State selection with autocomplete
 * - Form validation and error handling
 * - Dimension calculations and conversions
 * - Google Maps integration
 * - Regulation processing and calculations
 * - Results display and formatting
 * - Share, print, and report functionality
 * 
 * Dependencies:
 * - jQuery (for DOM manipulation)
 * - Google Maps API (for mapping features)
 * - state_regulations.js (for regulation data)
 * - Bootstrap (for styling - optional)
 */

// US States data for autocomplete
const US_STATES = [
    { name: 'Alabama', abbr: 'AL' },
    { name: 'Alaska', abbr: 'AK' },
    { name: 'Arizona', abbr: 'AZ' },
    { name: 'Arkansas', abbr: 'AR' },
    { name: 'California', abbr: 'CA' },
    { name: 'Colorado', abbr: 'CO' },
    { name: 'Connecticut', abbr: 'CT' },
    { name: 'Delaware', abbr: 'DE' },
    { name: 'Florida', abbr: 'FL' },
    { name: 'Georgia', abbr: 'GA' },
    { name: 'Hawaii', abbr: 'HI' },
    { name: 'Idaho', abbr: 'ID' },
    { name: 'Illinois', abbr: 'IL' },
    { name: 'Indiana', abbr: 'IN' },
    { name: 'Iowa', abbr: 'IA' },
    { name: 'Kansas', abbr: 'KS' },
    { name: 'Kentucky', abbr: 'KY' },
    { name: 'Louisiana', abbr: 'LA' },
    { name: 'Maine', abbr: 'ME' },
    { name: 'Maryland', abbr: 'MD' },
    { name: 'Massachusetts', abbr: 'MA' },
    { name: 'Michigan', abbr: 'MI' },
    { name: 'Minnesota', abbr: 'MN' },
    { name: 'Mississippi', abbr: 'MS' },
    { name: 'Missouri', abbr: 'MO' },
    { name: 'Montana', abbr: 'MT' },
    { name: 'Nebraska', abbr: 'NE' },
    { name: 'Nevada', abbr: 'NV' },
    { name: 'New Hampshire', abbr: 'NH' },
    { name: 'New Jersey', abbr: 'NJ' },
    { name: 'New Mexico', abbr: 'NM' },
    { name: 'New York', abbr: 'NY' },
    { name: 'North Carolina', abbr: 'NC' },
    { name: 'North Dakota', abbr: 'ND' },
    { name: 'Ohio', abbr: 'OH' },
    { name: 'Oklahoma', abbr: 'OK' },
    { name: 'Oregon', abbr: 'OR' },
    { name: 'Pennsylvania', abbr: 'PA' },
    { name: 'Rhode Island', abbr: 'RI' },
    { name: 'South Carolina', abbr: 'SC' },
    { name: 'South Dakota', abbr: 'SD' },
    { name: 'Tennessee', abbr: 'TN' },
    { name: 'Texas', abbr: 'TX' },
    { name: 'Utah', abbr: 'UT' },
    { name: 'Vermont', abbr: 'VT' },
    { name: 'Virginia', abbr: 'VA' },
    { name: 'Washington', abbr: 'WA' },
    { name: 'West Virginia', abbr: 'WV' },
    { name: 'Wisconsin', abbr: 'WI' },
    { name: 'Wyoming', abbr: 'WY' }
];

// Global variables
let selectedStates = [];
let currentSuggestionIndex = -1;
let suggestions = [];
let loadPlanMap;
let directionsService;
let directionsRenderer;
let originMarker;
let destinationMarker;

// DOM elements (will be set on DOM ready)
let stateSearchInput;
let selectedStatesContainer;
let clearAllButton;
let loadPlanForm;

// Initialize the load planning feature
document.addEventListener('DOMContentLoaded', function() {
    console.log('Load Planning JavaScript initializing...');
    
    // Set DOM element references
    stateSearchInput = document.getElementById('stateSearch');
    selectedStatesContainer = document.getElementById('selectedStates');
    clearAllButton = document.getElementById('clearAllStates');
    loadPlanForm = document.getElementById('loadPlanForm');
    
    // Check if required elements exist
    if (!stateSearchInput || !selectedStatesContainer || !loadPlanForm) {
        console.error('Required DOM elements not found for Load Planning');
        return;
    }
    
    // Initialize components
    setupStateAutocomplete();
    setupFormHandlers();
    
    // Initialize Google Maps after a delay to ensure API is loaded
    const isMobile = /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    const initialDelay = isMobile ? 1000 : 500;
    
    setTimeout(initMapAfterAPILoad, initialDelay);
    
    // Additional retry for mobile devices
    if (isMobile) {
        setTimeout(ensureMapLoaded, 3000);
    }
    
    console.log('Load Planning JavaScript initialized successfully');
});

/**
 * State Selection and Autocomplete Functions
 */
function setupStateAutocomplete() {
    if (!stateSearchInput) {
        console.error('State search input not found');
        return;
    }
    
    // Create suggestions dropdown
    const suggestionsDropdown = document.createElement('div');
    suggestionsDropdown.id = 'stateSuggestions';
    suggestionsDropdown.className = 'dropdown-menu w-100';
    suggestionsDropdown.style.cssText = 'position: absolute; top: 100%; left: 0; z-index: 1000; max-height: 200px; overflow-y: auto; display: none;';
    stateSearchInput.parentNode.style.position = 'relative';
    stateSearchInput.parentNode.appendChild(suggestionsDropdown);

    // Input event listener for autocomplete
    stateSearchInput.addEventListener('input', function(e) {
        const query = e.target.value.toLowerCase().trim();
        
        if (query.length === 0) {
            hideSuggestions();
            return;
        }

        // Filter states based on query
        suggestions = US_STATES.filter(state => {
            const alreadySelected = selectedStates.some(s => s.abbr === state.abbr);
            if (alreadySelected) return false;
            
            return state.name.toLowerCase().includes(query) || 
                   state.abbr.toLowerCase().includes(query);
        });

        showSuggestions(suggestions);
    });

    // Keyboard navigation
    stateSearchInput.addEventListener('keydown', function(e) {
        if (suggestions.length === 0) return;

        switch(e.key) {
            case 'ArrowDown':
                e.preventDefault();
                currentSuggestionIndex = Math.min(currentSuggestionIndex + 1, suggestions.length - 1);
                updateSuggestionHighlight();
                break;
                
            case 'ArrowUp':
                e.preventDefault();
                currentSuggestionIndex = Math.max(currentSuggestionIndex - 1, -1);
                updateSuggestionHighlight();
                break;
                
            case 'Enter':
                e.preventDefault();
                if (currentSuggestionIndex >= 0) {
                    selectState(suggestions[currentSuggestionIndex]);
                }
                break;
                
            case 'Escape':
                hideSuggestions();
                break;
        }
    });

    // Hide suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (!stateSearchInput.contains(e.target) && !document.getElementById('stateSuggestions').contains(e.target)) {
            hideSuggestions();
        }
    });

    // Clear all states button
    if (clearAllButton) {
        clearAllButton.addEventListener('click', function() {
            selectedStates = [];
            updateSelectedStatesDisplay();
            stateSearchInput.focus();
        });
    }
}

function showSuggestions(filteredStates) {
    const dropdown = document.getElementById('stateSuggestions');
    if (!dropdown) return;
    
    dropdown.innerHTML = '';
    currentSuggestionIndex = -1;

    if (filteredStates.length === 0) {
        dropdown.innerHTML = '<div class="dropdown-item-text text-muted">No states found</div>';
    } else {
        filteredStates.forEach((state, index) => {
            const item = document.createElement('button');
            item.type = 'button';
            item.className = 'dropdown-item';
            item.innerHTML = `<strong>${state.name}</strong> <small class="text-muted">(${state.abbr})</small>`;
            item.addEventListener('click', () => selectState(state));
            dropdown.appendChild(item);
        });
    }

    dropdown.style.display = 'block';
}

function hideSuggestions() {
    const dropdown = document.getElementById('stateSuggestions');
    if (dropdown) {
        dropdown.style.display = 'none';
    }
    currentSuggestionIndex = -1;
}

function updateSuggestionHighlight() {
    const dropdown = document.getElementById('stateSuggestions');
    if (!dropdown) return;
    
    const items = dropdown.querySelectorAll('.dropdown-item');
    
    items.forEach((item, index) => {
        if (index === currentSuggestionIndex) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
}

function selectState(state) {
    // Check if state is already selected
    if (selectedStates.some(s => s.abbr === state.abbr)) {
        return;
    }

    // Add state to selected states
    selectedStates.push(state);
    updateSelectedStatesDisplay();

    // Clear input and hide suggestions
    stateSearchInput.value = '';
    hideSuggestions();
    stateSearchInput.focus();
}

function removeState(stateAbbr) {
    selectedStates = selectedStates.filter(state => state.abbr !== stateAbbr);
    updateSelectedStatesDisplay();
}

function updateSelectedStatesDisplay() {
    if (!selectedStatesContainer) return;
    
    if (selectedStates.length === 0) {
        selectedStatesContainer.innerHTML = '<span class="text-muted">No states selected</span>';
        return;
    }

    selectedStatesContainer.innerHTML = selectedStates.map(state => `
        <span class="state-tag">
            ${state.abbr}
            <button type="button" class="remove-state" onclick="removeState('${state.abbr}')" title="Remove ${state.name}">
                ×
            </button>
        </span>
    `).join('');
}

/**
 * Form Handling and Validation Functions
 */
function setupFormHandlers() {
    if (!loadPlanForm) {
        console.error('Load plan form not found');
        return;
    }
    
    // Form submission handler
    loadPlanForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Clear previous errors
        clearValidationErrors();
        
        // Collect form data
        const formData = {
            origin: document.getElementById('origin')?.value?.trim() || '',
            destination: document.getElementById('destination')?.value?.trim() || '',
            roadType: document.querySelector('input[name="roadType"]:checked')?.value || 'Interstate',
            dimensions: {
                lengthFt: parseInt(document.getElementById('lengthFt')?.value) || 0,
                lengthIn: parseInt(document.getElementById('lengthIn')?.value) || 0,
                widthFt: parseInt(document.getElementById('widthFt')?.value) || 0,
                widthIn: parseInt(document.getElementById('widthIn')?.value) || 0,
                heightFt: parseInt(document.getElementById('heightFt')?.value) || 0,
                heightIn: parseInt(document.getElementById('heightIn')?.value) || 0,
                weight: parseInt(document.getElementById('weight')?.value) || 0
            },
            overhang: {
                frontFt: parseInt(document.getElementById('frontOverhangFt')?.value) || 0,
                frontIn: parseInt(document.getElementById('frontOverhangIn')?.value) || 0,
                rearFt: parseInt(document.getElementById('rearOverhangFt')?.value) || 0,
                rearIn: parseInt(document.getElementById('rearOverhangIn')?.value) || 0
            },
            states: selectedStates.map(s => s.abbr)
        };

        // Validate form
        const validationErrors = validateFormInputs(formData);
        if (!displayValidationErrors(validationErrors)) {
            return; // Stop if there are validation errors
        }

        console.log('Form Data:', formData);
        calculateEscortRequirements(formData);
    });
    
    // Initialize real-time validation
    addRealTimeValidation();
}

/**
 * Form Validation Functions
 */
function validateFormInputs(formData) {
    const errors = [];
    
    // Origin validation
    if (!formData.origin || formData.origin.length < 3) {
        errors.push({
            field: 'origin',
            message: 'Please enter a valid origin city and state'
        });
    }
    
    // Destination validation
    if (!formData.destination || formData.destination.length < 3) {
        errors.push({
            field: 'destination', 
            message: 'Please enter a valid destination city and state'
        });
    }
    
    // Dimension validation
    const dims = formData.dimensions;
    
    // Length validation
    if (dims.lengthFt < 0 || dims.lengthIn < 0 || dims.lengthIn > 11) {
        errors.push({
            field: 'length',
            message: 'Length must be positive and inches must be 0-11'
        });
    }
    if (dims.lengthFt === 0 && dims.lengthIn === 0) {
        errors.push({
            field: 'length',
            message: 'Please enter a valid length for your load'
        });
    }
    if (dims.lengthFt > 200) {
        errors.push({
            field: 'length',
            message: 'Length seems unusually large. Please verify your input'
        });
    }
    
    // Width validation  
    if (dims.widthFt < 0 || dims.widthIn < 0 || dims.widthIn > 11) {
        errors.push({
            field: 'width',
            message: 'Width must be positive and inches must be 0-11'
        });
    }
    if (dims.widthFt === 0 && dims.widthIn === 0) {
        errors.push({
            field: 'width',
            message: 'Please enter a valid width for your load'
        });
    }
    if (dims.widthFt > 30) {
        errors.push({
            field: 'width', 
            message: 'Width seems unusually large. Please verify your input'
        });
    }
    
    // Height validation
    if (dims.heightFt < 0 || dims.heightIn < 0 || dims.heightIn > 11) {
        errors.push({
            field: 'height',
            message: 'Height must be positive and inches must be 0-11'
        });
    }
    if (dims.heightFt === 0 && dims.heightIn === 0) {
        errors.push({
            field: 'height',
            message: 'Please enter a valid height for your load'
        });
    }
    if (dims.heightFt > 25) {
        errors.push({
            field: 'height',
            message: 'Height seems unusually large. Please verify your input'
        });
    }
    
    // Weight validation
    if (dims.weight < 0) {
        errors.push({
            field: 'weight',
            message: 'Weight must be positive'
        });
    }
    if (dims.weight === 0) {
        errors.push({
            field: 'weight',
            message: 'Please enter a valid weight for your load'
        });
    }
    if (dims.weight > 500000) {
        errors.push({
            field: 'weight',
            message: 'Weight seems unusually large. Please verify your input'
        });
    }
    
    // Overhang validation (if provided)
    if (formData.overhang.frontFt < 0 || formData.overhang.frontIn < 0 || 
        formData.overhang.rearFt < 0 || formData.overhang.rearIn < 0 ||
        formData.overhang.frontIn > 11 || formData.overhang.rearIn > 11) {
        errors.push({
            field: 'overhang',
            message: 'Overhang dimensions must be positive and inches must be 0-11'
        });
    }
    
    // States validation
    if (formData.states.length === 0) {
        errors.push({
            field: 'states',
            message: 'Please select at least one state for your route'
        });
    }
    
    return errors;
}

function displayValidationErrors(errors) {
    // Clear previous errors
    clearValidationErrors();
    
    if (errors.length === 0) return true;
    
    // Create error summary
    const errorSummary = document.createElement('div');
    errorSummary.id = 'validation-errors';
    errorSummary.className = 'alert alert-danger';
    errorSummary.innerHTML = `
        <h6><i class="fas fa-exclamation-triangle"></i> Please fix the following errors:</h6>
        <ul class="mb-0">
            ${errors.map(error => `<li>${error.message}</li>`).join('')}
        </ul>
    `;
    
    // Insert at top of form
    const formSection = document.querySelector('.form-section');
    if (formSection) {
        formSection.insertBefore(errorSummary, formSection.firstChild);
    }
    
    // Highlight error fields
    errors.forEach(error => {
        highlightErrorField(error.field);
    });
    
    // Scroll to errors
    errorSummary.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    return false;
}

function clearValidationErrors() {
    // Remove error summary
    const existingErrors = document.getElementById('validation-errors');
    if (existingErrors) {
        existingErrors.remove();
    }
    
    // Remove field highlights
    document.querySelectorAll('.form-control.is-invalid, .states-tags.is-invalid').forEach(field => {
        field.classList.remove('is-invalid');
    });
}

function highlightErrorField(fieldName) {
    let field;
    
    switch(fieldName) {
        case 'origin':
            field = document.getElementById('origin');
            break;
        case 'destination':
            field = document.getElementById('destination');
            break;
        case 'length':
            field = document.getElementById('lengthFt');
            break;
        case 'width':
            field = document.getElementById('widthFt');
            break;
        case 'height':
            field = document.getElementById('heightFt');
            break;
        case 'weight':
            field = document.getElementById('weight');
            break;
        case 'overhang':
            field = document.getElementById('frontOverhangFt');
            break;
        case 'states':
            field = document.getElementById('selectedStates');
            break;
    }
    
    if (field) {
        field.classList.add('is-invalid');
    }
}

function addRealTimeValidation() {
    // Add input event listeners for real-time validation
    const inputs = document.querySelectorAll('#loadPlanForm input[type="number"]');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            const value = parseFloat(this.value);
            
            // Remove invalid class first
            this.classList.remove('is-invalid');
            
            // Validate based on field
            if (this.id.includes('Ft') || this.id.includes('In')) {
                if (value < 0) {
                    this.classList.add('is-invalid');
                    this.title = 'Value must be positive';
                } else if (this.id.includes('In') && value > 11) {
                    this.classList.add('is-invalid');
                    this.title = 'Inches must be 0-11';
                } else {
                    this.title = '';
                }
            } else if (this.id === 'weight') {
                if (value < 0 || value > 500000) {
                    this.classList.add('is-invalid');
                    this.title = 'Weight must be between 0-500,000 lbs';
                } else {
                    this.title = '';
                }
            }
        });
    });
}

/**
 * Dimension Display and Calculation Functions
 */
function updateDimensionDisplay(dimensionType) {
    // Add a small delay to ensure input value is updated
    setTimeout(function() {
        const ftInput = document.getElementById(`${dimensionType}Ft`);
        const inInput = document.getElementById(`${dimensionType}In`);
        const totalDisplay = document.getElementById(`${dimensionType}Total`);
        
        if (!ftInput || !inInput || !totalDisplay) return;
        
        // Get current values, ensuring they're numbers
        let feet = parseInt(ftInput.value) || 0;
        let inches = parseInt(inInput.value) || 0;
        
        // Auto-convert excess inches to feet
        if (inches >= 12) {
            const extraFeet = Math.floor(inches / 12);
            const remainingInches = inches % 12;
            
            ftInput.value = feet + extraFeet;
            inInput.value = remainingInches;
            
            // Re-read the updated values
            feet = parseInt(ftInput.value) || 0;
            inches = parseInt(inInput.value) || 0;
        }
        
        // Display the same format as Route Summary: "X ft Y in"
        if (feet === 0 && inches === 0) {
            totalDisplay.textContent = '= 0 ft 0 in';
            totalDisplay.style.color = '#6c757d';
        } else {
            totalDisplay.textContent = `= ${feet} ft ${inches} in`;
            totalDisplay.style.color = 'var(--brand-primary)';
        }
    }, 50); // 50ms delay to ensure input is updated
}

/**
 * Regulation Processing and Calculation Functions
 */
function calculateEscortRequirements(formData) {
    // Show loading state
    const submitBtn = loadPlanForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Calculating...';
    submitBtn.disabled = true;

    // Process regulations
    setTimeout(() => {
        try {
            const results = processStateRegulations(formData);
            showResults(formData, results);
        } catch (error) {
            console.error('Error calculating escort requirements:', error);
            alert('Error calculating requirements. Please check your inputs and try again.');
        }
        
        // Reset button
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }, 500);
}

function processStateRegulations(formData) {
    const results = [];
    
    // Convert user dimensions to inches for comparison
    const userDimensions = {
        length: dimensionToInches(formData.dimensions.lengthFt, formData.dimensions.lengthIn),
        width: dimensionToInches(formData.dimensions.widthFt, formData.dimensions.widthIn),
        height: dimensionToInches(formData.dimensions.heightFt, formData.dimensions.heightIn),
        weight: formData.dimensions.weight,
        frontOverhang: dimensionToInches(formData.overhang.frontFt, formData.overhang.frontIn),
        rearOverhang: dimensionToInches(formData.overhang.rearFt, formData.overhang.rearIn)
    };
    
    // Calculate total overhang
    const totalOverhang = userDimensions.frontOverhang + userDimensions.rearOverhang;

    formData.states.forEach(stateAbbr => {
        const stateName = US_STATES.find(s => s.abbr === stateAbbr)?.name || stateAbbr;
        
        // Find all regulations for this state and road type
        const stateRegs = stateRegulations.filter(reg => 
            reg.state === stateName && reg.road_type === formData.roadType
        );

        if (stateRegs.length === 0) {
            results.push({
                state: stateAbbr,
                stateName: stateName,
                roadType: formData.roadType,
                routeSurvey: 'Unknown',
                policeEscort: 'Unknown',
                escortRequirements: 'No regulations found',
                notes: 'Contact state authorities for requirements'
            });
            return;
        }

        // Check each regulation rule for this state
        let applicableEscorts = new Set();
        let needsRouteSurvey = false;
        let needsPoliceEscort = false;
        let notes = [];

        stateRegs.forEach(reg => {
            let ruleApplies = false;

            // Check width requirements
            if (reg.width_min || reg.width_max) {
                if (compareDimension(userDimensions.width, reg.width_min, reg.width_max)) {
                    if (reg.width_escorts) {
                        applicableEscorts.add(reg.width_escorts);
                        ruleApplies = true;
                    }
                }
            }

            // Check length requirements
            if (reg.length_min || reg.length_max) {
                if (compareDimension(userDimensions.length, reg.length_min, reg.length_max)) {
                    if (reg.length_escorts) {
                        applicableEscorts.add(reg.length_escorts);
                        ruleApplies = true;
                    }
                }
            }

            // Check height requirements
            if (reg.height_min || reg.height_max) {
                if (compareDimension(userDimensions.height, reg.height_min, reg.height_max)) {
                    if (reg.height_escorts) {
                        applicableEscorts.add(reg.height_escorts);
                        ruleApplies = true;
                    }
                }
            }

            // Check weight requirements
            if (reg.weight_min || reg.weight_max) {
                if (compareWeight(userDimensions.weight, reg.weight_min, reg.weight_max)) {
                    if (reg.weight_escorts) {
                        applicableEscorts.add(reg.weight_escorts);
                        ruleApplies = true;
                    }
                }
            }

            // Check overhang requirements
            if (reg.overhang_min || reg.overhang_max) {
                if (compareDimension(totalOverhang, reg.overhang_min, reg.overhang_max)) {
                    if (reg.overhang_escorts) {
                        applicableEscorts.add(reg.overhang_escorts);
                        ruleApplies = true;
                    }
                }
            }

            // Check for route survey and police escort requirements
            if (ruleApplies) {
                Array.from(applicableEscorts).forEach(escort => {
                    if (escort && escort.toLowerCase().includes('route survey')) {
                        needsRouteSurvey = true;
                    }
                    if (escort && escort.toLowerCase().includes('police')) {
                        needsPoliceEscort = true;
                    }
                });

                // Add notes
                if (reg.notes) {
                    notes.push(reg.notes);
                }
            }
        });

        // Process escort requirements to remove duplicates and format
        let escortList = Array.from(applicableEscorts);
        if (escortList.length === 0) {
            escortList = ['None Required'];
        }

        results.push({
            state: stateAbbr,
            stateName: stateName,
            roadType: formData.roadType,
            routeSurvey: needsRouteSurvey ? 'Yes' : 'No',
            policeEscort: needsPoliceEscort ? 'Yes' : 'No', 
            escortRequirements: escortList.join(' + '),
            notes: notes.join('; ') || ''
        });
    });

    return results;
}

/**
 * Utility Functions for Regulation Processing
 */
function dimensionToInches(feet, inches) {
    return (feet * 12) + inches;
}

function parseDimension(dimensionStr) {
    if (!dimensionStr) return null;
    
    // Parse format like "12'6"" or "12'0""
    const match = dimensionStr.match(/(\d+)'(\d+)"/);
    if (match) {
        return dimensionToInches(parseInt(match[1]), parseInt(match[2]));
    }
    return null;
}

function compareWeight(weight, minWeight, maxWeight) {
    if (!weight) return false;
    if (minWeight && weight < parseInt(minWeight)) return false;
    if (maxWeight && weight > parseInt(maxWeight)) return false;
    return true;
}

function compareDimension(actualInches, minStr, maxStr) {
    if (!actualInches || actualInches === 0) return false;
    
    const minInches = parseDimension(minStr);
    const maxInches = parseDimension(maxStr);
    
    // Check if actual dimension falls within the range
    if (minInches && actualInches < minInches) return false;
    if (maxInches && actualInches > maxInches) return false;
    
    // If only min is specified and actual exceeds min
    if (minInches && !maxInches && actualInches >= minInches) return true;
    
    // If both min and max are specified and actual is in range
    if (minInches && maxInches && actualInches >= minInches && actualInches <= maxInches) return true;
    
    return false;
}

/**
 * Results Display Functions
 */
function showResults(formData, results) {
    const resultsSection = document.getElementById('resultsSection');
    const routeSummary = document.getElementById('routeSummary');
    const requirementsTable = document.getElementById('requirementsTable');
    
    if (!resultsSection || !routeSummary || !requirementsTable) {
        console.error('Results display elements not found');
        return;
    }
    
    // Store calculation data for potential reports
    window.lastCalculatedLoad = formData;
    
    // Convert dimensions to display format
    const length = `${formData.dimensions.lengthFt} ft ${formData.dimensions.lengthIn} in`;
    const width = `${formData.dimensions.widthFt} ft ${formData.dimensions.widthIn} in`;
    const height = `${formData.dimensions.heightFt} ft ${formData.dimensions.heightIn} in`;
    
    routeSummary.innerHTML = `
        <div class="route-summary">
            <h4><i class="fas fa-info-circle"></i> Route Summary</h4>
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Origin:</strong> ${formData.origin || 'Not specified'}</p>
                    <p><strong>Destination:</strong> ${formData.destination || 'Not specified'}</p>
                    <p><strong>Road Type:</strong> ${formData.roadType}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Length:</strong> ${length}</p>
                    <p><strong>Width:</strong> ${width}</p>
                    <p><strong>Height:</strong> ${height}</p>
                    <p><strong>Weight:</strong> ${formData.dimensions.weight.toLocaleString()} lbs</p>
                </div>
            </div>
            <p><strong>States:</strong> ${formData.states.join(' → ')}</p>
        </div>
    `;

    // Create requirements table
    const tableHTML = `
        <div class="requirements-table">
            <h5 class="section-title"><i class="fas fa-table"></i> Escort Requirements by State</h5>
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>State</th>
                            <th>Road Type</th>
                            <th>Route Survey</th>
                            <th>Police Escort</th>
                            <th>Escort Requirements</th>
                            <th>Notes</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${results.map(result => `
                            <tr>
                                <td><span class="badge bg-primary">${result.state}</span></td>
                                <td>${result.roadType}</td>
                                <td>${result.routeSurvey === 'Yes' ? '<span class="badge bg-warning">Yes</span>' : '<span class="badge bg-success">No</span>'}</td>
                                <td>${result.policeEscort === 'Yes' ? '<span class="badge bg-danger">Yes</span>' : '<span class="badge bg-success">No</span>'}</td>
                                <td>${result.escortRequirements}</td>
                                <td><small>${result.notes}</small></td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </div>
    `;

    requirementsTable.innerHTML = tableHTML + `
        <div class="results-actions">
            <button class="btn-share" onclick="shareResults()">
                <i class="fas fa-share-alt"></i> Share Results
            </button>
            <button class="btn-print" onclick="printResults()">
                <i class="fas fa-print"></i> Print Report
            </button>
            <button class="btn-report" onclick="reportIssue()">
                <i class="fas fa-flag"></i> Report Issue
            </button>
        </div>
        <div class="results-footer">
            <strong>Your App Name</strong> - Professional Load Planning | 
            <small>Generated by the Load Planning feature</small>
        </div>
    `;
    
    // Update map with route
    updateMapRoute(formData);
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Google Maps Integration Functions
 */
function initLoadPlanMap() {
    // Mobile-friendly map options
    const isMobile = /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    
    // Initialize map centered on US
    loadPlanMap = new google.maps.Map(document.getElementById('loadPlanMap'), {
        zoom: isMobile ? 3 : 4, // Slightly zoomed out for mobile
        center: { lat: 39.8283, lng: -98.5795 }, // Geographic center of US
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        gestureHandling: isMobile ? 'cooperative' : 'auto', // Better mobile scrolling
        disableDefaultUI: isMobile, // Clean interface on mobile
        zoomControl: true,
        mapTypeControl: !isMobile, // Hide on mobile to save space
        streetViewControl: false,
        fullscreenControl: !isMobile
    });

    // Initialize directions service and renderer
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer({
        suppressMarkers: false,
        draggable: false
    });
    directionsRenderer.setMap(loadPlanMap);
    
    // Initialize Google Places Autocomplete for Origin and Destination
    initializeCityAutocomplete();

    // Map type controls
    const mapTypeMap = document.getElementById('mapTypeMap');
    const mapTypeSatellite = document.getElementById('mapTypeSatellite');
    const resetMap = document.getElementById('resetMap');
    
    if (mapTypeMap) {
        mapTypeMap.addEventListener('change', function() {
            if (this.checked) {
                loadPlanMap.setMapTypeId(google.maps.MapTypeId.ROADMAP);
            }
        });
    }

    if (mapTypeSatellite) {
        mapTypeSatellite.addEventListener('change', function() {
            if (this.checked) {
                loadPlanMap.setMapTypeId(google.maps.MapTypeId.SATELLITE);
            }
        });
    }

    // Reset map button
    if (resetMap) {
        resetMap.addEventListener('click', function() {
            loadPlanMap.setCenter({ lat: 39.8283, lng: -98.5795 });
            loadPlanMap.setZoom(4);
            clearMapMarkers();
        });
    }
}

function clearMapMarkers() {
    if (originMarker) originMarker.setMap(null);
    if (destinationMarker) destinationMarker.setMap(null);
    if (directionsRenderer) directionsRenderer.set('directions', null);
}

function updateMapRoute(formData) {
    if (!loadPlanMap || !directionsService || !directionsRenderer) {
        console.log('Google Maps not yet initialized, skipping map update');
        return;
    }

    const origin = formData.origin;
    const destination = formData.destination;

    if (!origin || !destination) {
        console.log('Origin or destination not specified, skipping map update');
        return;
    }

    // Clear existing markers and routes
    clearMapMarkers();

    // Calculate and display route
    const request = {
        origin: origin,
        destination: destination,
        travelMode: google.maps.TravelMode.DRIVING,
        avoidHighways: formData.roadType === 'Non-Interstate',
        optimizeWaypoints: false
    };

    directionsService.route(request, function(result, status) {
        if (status === 'OK') {
            directionsRenderer.setDirections(result);
            
            // Add custom markers for origin and destination
            addCustomMarkers(result.routes[0]);
            
        } else {
            console.warn('Directions request failed:', status);
            
            // Fallback: try to geocode and add individual markers
            geocodeAndAddMarkers(origin, destination);
        }
    });
}

function addCustomMarkers(route) {
    const leg = route.legs[0];
    
    // Origin marker
    originMarker = new google.maps.Marker({
        position: leg.start_location,
        map: loadPlanMap,
        title: 'Origin',
        icon: {
            url: 'https://maps.google.com/mapfiles/ms/icons/green-dot.png',
            scaledSize: new google.maps.Size(32, 32)
        }
    });

    // Destination marker
    destinationMarker = new google.maps.Marker({
        position: leg.end_location,
        map: loadPlanMap,
        title: 'Destination',
        icon: {
            url: 'https://maps.google.com/mapfiles/ms/icons/red-dot.png',
            scaledSize: new google.maps.Size(32, 32)
        }
    });
}

function geocodeAndAddMarkers(origin, destination) {
    const geocoder = new google.maps.Geocoder();
    
    // Geocode origin
    geocoder.geocode({ address: origin }, function(results, status) {
        if (status === 'OK') {
            originMarker = new google.maps.Marker({
                position: results[0].geometry.location,
                map: loadPlanMap,
                title: 'Origin: ' + origin,
                icon: {
                    url: 'https://maps.google.com/mapfiles/ms/icons/green-dot.png',
                    scaledSize: new google.maps.Size(32, 32)
                }
            });
            
            loadPlanMap.setCenter(results[0].geometry.location);
            loadPlanMap.setZoom(6);
        }
    });
    
    // Geocode destination
    geocoder.geocode({ address: destination }, function(results, status) {
        if (status === 'OK') {
            destinationMarker = new google.maps.Marker({
                position: results[0].geometry.location,
                map: loadPlanMap,
                title: 'Destination: ' + destination,
                icon: {
                    url: 'https://maps.google.com/mapfiles/ms/icons/red-dot.png',
                    scaledSize: new google.maps.Size(32, 32)
                }
            });
        }
    });
}

function initializeCityAutocomplete() {
    // Configure autocomplete options
    const autocompleteOptions = {
        types: ['(cities)'], // Restrict to cities
        componentRestrictions: { country: 'us' }, // Restrict to US
        fields: ['formatted_address', 'geometry', 'name']
    };

    // Initialize autocomplete for origin field
    const originInput = document.getElementById('origin');
    const destinationInput = document.getElementById('destination');
    
    if (originInput && typeof google !== 'undefined' && google.maps && google.maps.places) {
        const originAutocomplete = new google.maps.places.Autocomplete(originInput, autocompleteOptions);
        
        // Optional: Add place change listeners for future enhancements
        originAutocomplete.addListener('place_changed', function() {
            const place = originAutocomplete.getPlace();
            if (place.geometry) {
                console.log('Origin selected:', place.formatted_address);
            }
        });
    }
    
    if (destinationInput && typeof google !== 'undefined' && google.maps && google.maps.places) {
        const destinationAutocomplete = new google.maps.places.Autocomplete(destinationInput, autocompleteOptions);
        
        destinationAutocomplete.addListener('place_changed', function() {
            const place = destinationAutocomplete.getPlace();
            if (place.geometry) {
                console.log('Destination selected:', place.formatted_address);
            }
        });
    }

    console.log('City autocomplete initialized for Origin and Destination fields');
}

function initMapAfterAPILoad() {
    if (typeof google !== 'undefined' && google.maps && google.maps.Map) {
        initLoadPlanMap();
        console.log('Load Plan map initialized successfully');
    } else {
        // Wait for Google Maps API to load (longer timeout for mobile)
        setTimeout(initMapAfterAPILoad, 200);
    }
}

function ensureMapLoaded() {
    const mapContainer = document.getElementById('loadPlanMap');
    if (mapContainer && !window.loadPlanMap) {
        console.log('Retrying map initialization for mobile...');
        initMapAfterAPILoad();
    }
}

/**
 * Share, Print, and Report Functions
 */
function shareResults() {
    // Create shareable data
    const resultsSection = document.getElementById('resultsSection');
    if (!resultsSection || resultsSection.style.display === 'none') {
        alert('Please calculate escort requirements first!');
        return;
    }
    
    // Create share text
    const currentUrl = window.location.origin + window.location.pathname;
    const shareText = `Check out my Load Planning Report!\n\n` +
                     `🚛 Professional escort requirements calculated\n` +
                     `📍 Detailed route analysis\n` +
                     `✅ State-by-state regulations\n\n` +
                     `Calculate your own load requirements at: ${currentUrl}\n\n` +
                     `#LoadPlanning #OversizedLoad #EscortServices`;
    
    // Try to use Web Share API (mobile)
    if (navigator.share) {
        navigator.share({
            title: 'Load Planning Report',
            text: shareText,
            url: currentUrl
        }).then(() => {
            console.log('Successfully shared');
        }).catch((error) => {
            console.log('Error sharing:', error);
            fallbackShare(shareText);
        });
    } else {
        // Fallback for desktop
        fallbackShare(shareText);
    }
}

function fallbackShare(shareText) {
    // Copy to clipboard
    if (navigator.clipboard) {
        navigator.clipboard.writeText(shareText).then(() => {
            showShareModal(shareText);
        }).catch(() => {
            showShareModal(shareText);
        });
    } else {
        showShareModal(shareText);
    }
}

function showShareModal(shareText) {
    const modal = `
        <div id="shareModal" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
             background: rgba(0,0,0,0.5); z-index: 10000; display: flex; align-items: center; justify-content: center;">
            <div style="background: white; padding: 30px; border-radius: 12px; max-width: 500px; width: 90%; 
                 box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
                <h4 style="color: var(--brand-primary); margin-bottom: 20px;">
                    <i class="fas fa-share-alt"></i> Share Your Load Planning Report
                </h4>
                <textarea readonly style="width: 100%; height: 150px; border: 1px solid #ddd; 
                         border-radius: 8px; padding: 15px; font-size: 14px; resize: none;">${shareText}</textarea>
                <div style="margin-top: 20px; text-align: center;">
                    <small style="color: #666; margin-bottom: 15px; display: block;">
                        Text copied to clipboard! You can paste it anywhere.
                    </small>
                    <button onclick="closeShareModal()" style="background: var(--brand-primary); color: white; 
                           border: none; padding: 10px 25px; border-radius: 8px; font-weight: 600;">
                        Close
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modal);
}

function closeShareModal() {
    const modal = document.getElementById('shareModal');
    if (modal) {
        modal.remove();
    }
}

function printResults() {
    const resultsSection = document.getElementById('resultsSection');
    if (!resultsSection || resultsSection.style.display === 'none') {
        alert('Please calculate escort requirements first!');
        return;
    }
    
    // Trigger print
    window.print();
}

function reportIssue() {
    const resultsSection = document.getElementById('resultsSection');
    if (!resultsSection || resultsSection.style.display === 'none') {
        alert('Please calculate escort requirements first!');
        return;
    }

    // Get current load info for context
    const formData = {
        origin: document.getElementById('origin')?.value || '',
        destination: document.getElementById('destination')?.value || '',
        roadType: document.querySelector('input[name="roadType"]:checked')?.value || '',
        customRoute: Array.from(document.querySelectorAll('.state-tag')).map(tag => tag.textContent.replace('×', '').trim()),
        lengthFt: document.getElementById('lengthFt')?.value || '0',
        lengthIn: document.getElementById('lengthIn')?.value || '0',
        widthFt: document.getElementById('widthFt')?.value || '0',
        widthIn: document.getElementById('widthIn')?.value || '0',
        heightFt: document.getElementById('heightFt')?.value || '0',
        heightIn: document.getElementById('heightIn')?.value || '0',
        weight: document.getElementById('weight')?.value || '0'
    };
    
    showReportModal(formData);
}

function showReportModal(loadData) {
    const modal = `
        <div id="reportModal" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
             background: rgba(0,0,0,0.5); z-index: 10000; display: flex; align-items: center; justify-content: center;">
            <div style="background: white; padding: 30px; border-radius: 12px; max-width: 600px; width: 90%; 
                 max-height: 90vh; overflow-y: auto; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
                <h4 style="color: var(--brand-primary); margin-bottom: 20px;">
                    <i class="fas fa-flag"></i> Report Regulation Issue
                </h4>
                
                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-size: 14px;">
                    <strong>Load Details:</strong><br>
                    Route: ${loadData.origin} → ${loadData.destination}<br>
                    States: ${loadData.customRoute.join(', ')}<br>
                    Dimensions: ${loadData.lengthFt}'${loadData.lengthIn}" L × ${loadData.widthFt}'${loadData.widthIn}" W × ${loadData.heightFt}'${loadData.heightIn}" H<br>
                    Weight: ${loadData.weight} lbs | Road Type: ${loadData.roadType}
                </div>
                
                <form id="reportForm" style="margin-bottom: 20px;">
                    <div style="margin-bottom: 15px;">
                        <label style="display: block; font-weight: 600; margin-bottom: 8px;">Issue Type:</label>
                        <select id="issueType" required style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px;">
                            <option value="">Select issue type...</option>
                            <option value="incorrect_escort">Incorrect escort requirement</option>
                            <option value="missing_state">Missing state regulation</option>
                            <option value="outdated_rule">Outdated regulation</option>
                            <option value="calculation_error">Calculation error</option>
                            <option value="other">Other</option>
                        </select>
                    </div>
                    
                    <div style="margin-bottom: 15px;">
                        <label style="display: block; font-weight: 600; margin-bottom: 8px;">Which State(s)?</label>
                        <input type="text" id="affectedStates" placeholder="e.g., NC, SC, GA" 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px;">
                    </div>
                    
                    <div style="margin-bottom: 15px;">
                        <label style="display: block; font-weight: 600; margin-bottom: 8px;">Description:</label>
                        <textarea id="issueDescription" required placeholder="Please describe the issue in detail..." 
                                  style="width: 100%; height: 100px; padding: 10px; border: 1px solid #ddd; border-radius: 6px; resize: vertical;"></textarea>
                    </div>
                    
                    <div style="margin-bottom: 15px;">
                        <label style="display: block; font-weight: 600; margin-bottom: 8px;">Your Contact (Optional):</label>
                        <input type="email" id="reporterEmail" placeholder="your@email.com" 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px;">
                        <small style="color: #666; display: block; margin-top: 5px;">
                            We'll only use this to follow up on your report
                        </small>
                    </div>
                </form>
                
                <div style="text-align: center; display: flex; gap: 15px; justify-content: center;">
                    <button onclick="submitReport()" style="background: var(--brand-primary); color: white; 
                           border: none; padding: 12px 25px; border-radius: 8px; font-weight: 600;">
                        Submit Report
                    </button>
                    <button onclick="closeReportModal()" style="background: #6c757d; color: white; 
                           border: none; padding: 12px 25px; border-radius: 8px; font-weight: 600;">
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modal);
}

function submitReport() {
    const form = document.getElementById('reportForm');
    const issueType = document.getElementById('issueType')?.value;
    const description = document.getElementById('issueDescription')?.value;
    
    if (!issueType || !description) {
        alert('Please fill in all required fields!');
        return;
    }
    
    const reportData = {
        issueType: issueType,
        affectedStates: document.getElementById('affectedStates')?.value || '',
        description: description,
        reporterEmail: document.getElementById('reporterEmail')?.value || '',
        loadData: window.lastCalculatedLoad || {},
        timestamp: new Date().toISOString()
    };
    
    // Disable submit button to prevent double submission
    const submitBtn = document.querySelector('button[onclick="submitReport()"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Submitting...';
    submitBtn.disabled = true;
    
    // Send report to backend (adjust URL as needed)
    fetch('/load-planning/api/submit-report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(reportData)
    })
    .then(response => response.json())
    .then(data => {
        closeReportModal();
        if (data.success) {
            alert(data.message || 'Thank you! Your report has been submitted and emailed to our admin team.');
        } else {
            alert(data.error || 'Failed to submit report. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error submitting report:', error);
        closeReportModal();
        alert('Network error. Please check your connection and try again.');
    })
    .finally(() => {
        // Re-enable submit button
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    });
}

function closeReportModal() {
    const modal = document.getElementById('reportModal');
    if (modal) {
        modal.remove();
    }
}

// Export functions for global access
window.updateDimensionDisplay = updateDimensionDisplay;
window.removeState = removeState;
window.shareResults = shareResults;
window.printResults = printResults;
window.reportIssue = reportIssue;
window.submitReport = submitReport;
window.closeShareModal = closeShareModal;
window.closeReportModal = closeReportModal;

console.log('Load Planning JavaScript implementation loaded successfully');
