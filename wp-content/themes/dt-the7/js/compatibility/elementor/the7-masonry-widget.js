jQuery(window).on("elementor/frontend/init", function () {
    elementorFrontend.hooks.addAction("frontend/element_ready/the7_elements.default", function ($scope) {
        var $isoContainer = $scope.find(".iso-container");
        var $gridContainer = $scope.find(".jquery-filter .dt-css-grid");

        if ($isoContainer.length) {
            the7ApplyColumns($scope.attr("data-id"), $isoContainer, the7GetElementorMasonryColumnsConfig);
        } else if ($gridContainer.length) {
            the7ApplyMasonryWidgetCSSGridFiltering($gridContainer);
        }
    });
});