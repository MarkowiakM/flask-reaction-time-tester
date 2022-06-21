const SUBMIT_BUTTON = document.querySelector('.submit');
const FORM = document.querySelector('.result-form');
const RESULT_INPUT = document.querySelector('.result-input');
const TEST_PANEL = document.querySelector('.tester');
const SPAN_INFO = document.querySelector('.info');
const RESULT_SPANS = [...document.querySelectorAll('span.single-result')];
const MIN_WAIT_TIME = 500;
const MAX_WAIT_TIME = 2000;

let trials = 5;
let results = [];
let trialStart = 0;
let trialEnd = 0;
let trialCounter = 0;
let timeout = 0;


/**
 * changeColor - changes the color of html test panel
 * @param {String} color - name of class that is added to the test panel (red, blue or green)
 */
const changeColor = (color) => {
    TEST_PANEL.classList.remove(TEST_PANEL.id);
    TEST_PANEL.id = color;
    TEST_PANEL.classList.add(color);
}


/**
 * getMean - returns the arithemtic mean of the time results 
 * @return {[Number]} arithmetic mean
 */
const getMean = () => {
    return results.reduce((acc, curr) => acc + curr) / trials;
}

/**
 * updateResultSpans - updates the result spans with the result messages
 */
const updateResultSpans = () => {
    RESULT_SPANS.forEach((div, i) => {
        if (results[i]) {
            div.textContent = `${results[i]} ms`;
        }
    })
}

/**
 * clearResultSpans - clears the result spans
 */
const clearResultSpans = () => {
    RESULT_SPANS.forEach((div) => {
        div.textContent = '';
    })
    document.querySelector('span.final-result').textContent = 'avg:';

}

/**
 * reset - resets all game testing params and result spans
 */
function reset() {
    trials = 5;
    results = []
    trialStart = 0;
    trialEnd = 0;
    trialCounter = 0;
    timeout = 0;
    clearResultSpans()
    SPAN_INFO.textContent = 'Click to start';
    TEST_PANEL.onclick = startTesting;
}

/**
 * setTrialTimeout - sets a random time to wait for a green panel 
 */
const setTrialTimeout = () => { timeout = setTimeout(startTimer, Math.floor(Math.random() * MAX_WAIT_TIME + MIN_WAIT_TIME)); }

/**
 * startTesting - sets test panel's onclick method to falseStart, starts next trial
 */
const startTesting = () => {
    if (trialCounter < trials) {
        changeColor('red');
        SPAN_INFO.textContent = 'Wait for green...';
        TEST_PANEL.onclick = falseStart;
        trialCounter++;
        setTrialTimeout();
    }
}

/**
 * falseStart - clears timeout before the next trial and sets time result to 2s
 */
function falseStart() {
    clearTimeout(timeout);
    trialStart = new Date().getTime() - 2000;
    stopTimer();
}

/**
 * startTimer - starts measuring the reaction time, sets onlick method to stopTimer
 */
function startTimer() {
    changeColor('green');
    SPAN_INFO.textContent = '';
    TEST_PANEL.onclick = stopTimer;
    trialStart = new Date().getTime();
}

/**
 * updateSingleResult -updates results list with a single result's time
 */
function updateSingleResult() {
    trialEnd = new Date().getTime() - trialStart;
    results[trialCounter - 1] = trialEnd;
}

/**
 * stopTimer - sets onlick method to startTesting and stops the trial
 */
function stopTimer() {
    updateSingleResult();
    changeColor('blue');
    updateResultSpans();
    TEST_PANEL.onclick = startTesting;
    SPAN_INFO.textContent = 'Click to start';
    if (trialCounter >= trials) {
        SPAN_INFO.textContent = '';
        document.querySelector('span.final-result').textContent += ` ${getMean().toFixed(1)} ms`;
        RESULT_INPUT.value = `${getMean().toFixed(1)}`;
        FORM.style.display = 'flex';
        TEST_PANEL.style.display = 'none';
        RESULT_INPUT.style.display = 'none';
    }
}

document.querySelector('.blue').onclick = startTesting;
