
var stringUtils = {};

stringUtils.isEmpty = function(val) {

	if(val === null || val === undefined || val === NaN || val.trim() === "" ) {
		return true;
	} else {
		return false;
	}

};


module.exports = stringUtils;
