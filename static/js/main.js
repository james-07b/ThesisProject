(function () {
    function calculateBmr(weight, height, age) {
    weight = parseFloat(weight);
    height = parseFloat(height);
    age = parseFloat(age);
    bmr = ((weight * 10) + (height * 6.25) - (age *5) + 5);
    return bmr;
    }
    
    var bmr = document.getElementById("bmr");
    if (bmr) {
    bmr.onsubmit = function () {
      this.result.value = calculateBmr(this.weight.value, this.height.value, this.age.value);
      return false;
    };
    }
    function calculateCals(activity) {
    activity = parseFloat(activity);
    cals = ((bmr * activity));
    return cals;
    }
    var cals = document.getElementById("cals");
    if (cals) {
    cals.onsubmit = function () {
      this.result.value = calculateCals(this.activity.value);
      return false;
    };
    }
    }());
    
    (function () {
    function MacrosToCalories(proteins, carbs, fats) {
    proteins = parseFloat(proteins);
    carbs = parseFloat(carbs);
    fats = parseFloat(fats);
    return ((proteins * 4) + (carbs * 4) + (fats * 9));
    }
    
    var calculateMacros = document.getElementById("calculateMacros");
    if (calculateMacros) {
    calculateMacros.onsubmit = function () {
      this.result.value = MacrosToCalories(this.proteins.value, this.carbs.value, this.fats.value);
      return false;
    };
    }
    }());