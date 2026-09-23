    var viewer_modal;
    $(function() {
        viewer_modal = $('#imageViewerModal')
        $('.img-item').click(function() {
            if($(this).find('.img-thumb').attr('data-is-dir') == "False")
            {
                viewer_modal.find('#img-viewer').attr('src', $(this).find('.img-thumb').attr('data-full-size'))
                viewer_modal.modal('show')
            }
            else
            {
                $(this).on("click", function() { window.location.href = $(this).find('.img-thumb').attr('data-full-size') })
            }
        })
        viewer_modal.on('hidden.bs.modal', function() {
            viewer_modal.find('#img-viewer').attr('src', '')
        })

        $('.control-next').click(function() {
            var cur_img = viewer_modal.find('#img-viewer').attr('src');
            var index = $('.img-thumb[src="' + cur_img + '"]').closest('.img-item').index() + 1;
            var next_index = index > ($('.img-thumb').length - 1) ? 0 : index;
            viewer_modal.find('#img-viewer').attr('src', $('.img-thumb').eq(next_index).attr('data-full-size'))
        })

        $('.control-prev').click(function() {
            var cur_img = viewer_modal.find('#img-viewer').attr('src');
            var index = $('.img-thumb[src="' + cur_img + '"]').closest('.img-item').index() - 1;
            var prev_index = index < 0 ? ($('.img-thumb').length - 1) : index;
            viewer_modal.find('#img-viewer').attr('src', $('.img-thumb').eq(prev_index).attr('data--full-size'))
        })
    })
