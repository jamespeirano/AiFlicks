$(document).ready(function() {
    $('#prompt').on('submit', function() {
        // Collect checkbox values
        var photorealistic = $('#photorealistic-checkbox').is(':checked');
        var semantic = $('#semantic-checkbox').is(':checked');
        var coherence = $('#coherence-checkbox').is(':checked');
        var novelty = $('#novelty-checkbox').is(':checked');

        // Set checkbox values in hidden inputs
        $('input[name="photorealistic"]').val(photorealistic);
        $('input[name="semantic"]').val(semantic);
        $('input[name="coherence"]').val(coherence);
        $('input[name="novelty"]').val(novelty);

        // Submit the form
        return true;
    });
});
