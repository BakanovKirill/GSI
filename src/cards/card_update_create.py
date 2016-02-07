# -*- coding: utf-8 -*-
from cards.models import (QRF, RFScore, Remap,
                          YearFilter, Collate, PreProc,
                          MergeCSV, RFTrain)




def qrf_update_create(form, item_id=None):
    if item_id:
        QRF.objects.filter(id=item_id).update(
            name=form.cleaned_data["name"],
            interval=form.cleaned_data["interval"],
            number_of_trees=form.cleaned_data["number_of_trees"],
            number_of_threads=form.cleaned_data["number_of_threads"],
            directory=form.cleaned_data["directory"],
        )
        qrf_card = QRF.objects.get(id=item_id)
    else:
        qrf_card = QRF.objects.create(
            name=form.cleaned_data["name"],
            interval=form.cleaned_data["interval"],
            number_of_trees=form.cleaned_data["number_of_trees"],
            number_of_threads=form.cleaned_data["number_of_threads"],
            directory=form.cleaned_data["directory"],
        )

    return qrf_card


def rfscore_update_create(form, item_id=None):
    if item_id:
        RFScore.objects.filter(id=item_id).update(
            name=form.cleaned_data["name"],
            area=form.cleaned_data["area"],
            year_group=form.cleaned_data["year_group"],
            bias_corrn=form.cleaned_data["bias_corrn"],
            number_of_threads=form.cleaned_data["number_of_threads"],
            QRFopts=form.cleaned_data["QRFopts"],
            ref_target=form.cleaned_data["ref_target"],
            clean_name=form.cleaned_data["clean_name"],
            run_parallel=form.cleaned_data["run_parallel"],
        )
        rfscore_card = RFScore.objects.get(id=item_id)
    else:
        rfscore_card = RFScore.objects.create(
            name=form.cleaned_data["name"],
            area=form.cleaned_data["area"],
            year_group=form.cleaned_data["year_group"],
            bias_corrn=form.cleaned_data["bias_corrn"],
            number_of_threads=form.cleaned_data["number_of_threads"],
            QRFopts=form.cleaned_data["QRFopts"],
            ref_target=form.cleaned_data["ref_target"],
            clean_name=form.cleaned_data["clean_name"],
            run_parallel=form.cleaned_data["run_parallel"],
        )

    return rfscore_card


def remap_update_create(form, item_id=None):
    if item_id:
        Remap.objects.filter(id=item_id).update(
            name=form.cleaned_data["name"],
            file_spec=form.cleaned_data["file_spec"],
            roi=form.cleaned_data["roi"],
            output_root=form.cleaned_data["output_root"],
            output_suffix=form.cleaned_data["output_suffix"],
            scale=form.cleaned_data["scale"],
            output=form.cleaned_data["output"],
            color_table=form.cleaned_data["color_table"],
            refstats_file=form.cleaned_data["refstats_file"],
            refstats_scale=form.cleaned_data["refstats_scale"],
            run_parallel=form.cleaned_data["run_parallel"],
        )
        remap_card = Remap.objects.get(id=item_id)
    else:
        remap_card = Remap.objects.create(
            name=form.cleaned_data["name"],
            file_spec=form.cleaned_data["file_spec"],
            roi=form.cleaned_data["roi"],
            output_root=form.cleaned_data["output_root"],
            output_suffix=form.cleaned_data["output_suffix"],
            scale=form.cleaned_data["scale"],
            output=form.cleaned_data["output"],
            color_table=form.cleaned_data["color_table"],
            refstats_file=form.cleaned_data["refstats_file"],
            refstats_scale=form.cleaned_data["refstats_scale"],
            run_parallel=form.cleaned_data["run_parallel"],
        )

    return remap_card


def year_filter_update_create(form, item_id=None):
    if item_id:
        YearFilter.objects.filter(id=item_id).update(
            name=form.cleaned_data["name"],
            area=form.cleaned_data["area"],
            filetype=form.cleaned_data["filetype"],
            filter=form.cleaned_data["filter"],
            filter_output=form.cleaned_data["filter_output"],
            extend_start=form.cleaned_data["extend_start"],
            input_fourier=form.cleaned_data["input_fourier"],
            output_directory=form.cleaned_data["output_directory"],
            input_directory=form.cleaned_data["input_directory"],
            run_parallel=form.cleaned_data["run_parallel"],
        )
        year_filter_card = YearFilter.objects.get(id=item_id)
    else:
        year_filter_card = YearFilter.objects.create(
            name=form.cleaned_data["name"],
            area=form.cleaned_data["area"],
            filetype=form.cleaned_data["filetype"],
            filter=form.cleaned_data["filter"],
            filter_output=form.cleaned_data["filter_output"],
            extend_start=form.cleaned_data["extend_start"],
            input_fourier=form.cleaned_data["input_fourier"],
            output_directory=form.cleaned_data["output_directory"],
            input_directory=form.cleaned_data["input_directory"],
            run_parallel=form.cleaned_data["run_parallel"],
        )

    return year_filter_card


def collate_update_create(form, item_id=None):
    if item_id:
        Collate.objects.filter(id=item_id).update(
            name=form.cleaned_data["name"],
            area=form.cleaned_data["area"],
            mode=form.cleaned_data["mode"],
            input_file=form.cleaned_data["input_file"],
            output_tile_subdir=form.cleaned_data["output_tile_subdir"],
            input_scale_factor=form.cleaned_data["input_scale_factor"],
            run_parallel=form.cleaned_data["run_parallel"],
        )
        collate_card = Collate.objects.get(id=item_id)
    else:
        collate_card = Collate.objects.create(
            name=form.cleaned_data["name"],
            area=form.cleaned_data["area"],
            mode=form.cleaned_data["mode"],
            input_file=form.cleaned_data["input_file"],
            output_tile_subdir=form.cleaned_data["output_tile_subdir"],
            input_scale_factor=form.cleaned_data["input_scale_factor"],
            run_parallel=form.cleaned_data["run_parallel"],
        )

    return collate_card


def preproc_update_create(form, item_id=None):
    if item_id:
        PreProc.objects.filter(id=item_id).update(
            name=form.cleaned_data["name"],
            area=form.cleaned_data["area"],
            mode=form.cleaned_data["mode"],
            year_group=form.cleaned_data["year_group"],
            run_parallel=form.cleaned_data["run_parallel"],
        )
        preproc_card = PreProc.objects.get(id=item_id)
    else:
        preproc_card = PreProc.objects.create(
            name=form.cleaned_data["name"],
            area=form.cleaned_data["area"],
            mode=form.cleaned_data["mode"],
            year_group=form.cleaned_data["year_group"],
            run_parallel=form.cleaned_data["run_parallel"],
        )

    return preproc_card


def mergecsv_update_create(form, item_id=None):
    if item_id:
        MergeCSV.objects.filter(id=item_id).update(
            name=form.cleaned_data["name"],
            csv1=form.cleaned_data["csv1"],
            csv2=form.cleaned_data["csv2"],
        )
        mergecsv_card = MergeCSV.objects.get(id=item_id)
    else:
        mergecsv_card = MergeCSV.objects.create(
            name=form.cleaned_data["name"],
            csv1=form.cleaned_data["csv1"],
            csv2=form.cleaned_data["csv2"],
        )

    return mergecsv_card


def rftrain_update_create(form, item_id=None):
    if item_id:
        RFTrain.objects.filter(id=item_id).update(
            name=form.cleaned_data["name"],
            tile_type=form.cleaned_data["tile_type"],
            number_of_trees=form.cleaned_data["number_of_trees"],
            value=form.cleaned_data["value"],
            config_file=form.cleaned_data["config_file"],
            output_tile_subdir=form.cleaned_data["output_tile_subdir"],
            input_scale_factor=form.cleaned_data["input_scale_factor"],
            run_parallel=form.cleaned_data["run_parallel"],
        )
        rftrain_card = RFTrain.objects.get(id=item_id)
    else:
        rftrain_card = RFTrain.objects.create(
            name=form.cleaned_data["name"],
            tile_type=form.cleaned_data["tile_type"],
            number_of_trees=form.cleaned_data["number_of_trees"],
            value=form.cleaned_data["value"],
            config_file=form.cleaned_data["config_file"],
            output_tile_subdir=form.cleaned_data["output_tile_subdir"],
            input_scale_factor=form.cleaned_data["input_scale_factor"],
            run_parallel=form.cleaned_data["run_parallel"],
        )

    return rftrain_card
