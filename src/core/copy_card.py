# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404

from cards.models import (QRF, RFScore, Remap,
                          YearFilter, Collate, PreProc,
                          MergeCSV, RFTrain, RandomForest,
                          CalcStats)


COPY_CARD = {

}


def qrf_copy(card):
    name = ''
    qrf_card = QRF.objects.create(
        name=name,
        interval=card.interval,
        number_of_trees=card.number_of_trees,
        number_of_threads=card.number_of_threads,
        directory=card.directory,
    )

    return qrf_card


def rfscore_copy(name, card):
    rfscore_card = RFScore.objects.create(
        name=name,
        area=card.area,
        year_group=card.year_group,
        bias_corrn=card.bias_corrn,
        number_of_threads=card.number_of_threads,
        QRFopts=card.QRFopts,
        ref_target=card.cleaned_data["ref_target"],
        clean_name=card.cleaned_data["clean_name"],
        run_parallel=card.cleaned_data["run_parallel"],
    )

    return rfscore_card


def remap_update_create(name, card):
    remap_card = Remap.objects.create(
        name=card.cleaned_data["name"],
        run_parallel=card.cleaned_data["run_parallel"],
        file_spec=card.cleaned_data["file_spec"],
        roi=card.cleaned_data["roi"],
        year_group=card.cleaned_data["year_group"],
        model_name=card.cleaned_data["model_name"],
        output_root=card.cleaned_data["output_root"],
        output_suffix=card.cleaned_data["output_suffix"],
        scale=card.cleaned_data["scale"],
        output=card.cleaned_data["output"],
        color_table=card.cleaned_data["color_table"],
        refstats_file=card.cleaned_data["refstats_file"],
        refstats_scale=card.cleaned_data["refstats_scale"],
        conditional_mean=card.cleaned_data["conditional_mean"],
        conditional_min=card.cleaned_data["conditional_min"],
        conditional_median=card.cleaned_data["conditional_median"],
        conditional_max=card.cleaned_data["conditional_max"],
        lower_quartile=card.cleaned_data["lower_quartile"],
        upper_quartile=card.cleaned_data["upper_quartile"],
    )

    return remap_card


def year_filter_update_create(name, card):
    year_filter_card = YearFilter.objects.create(
        name=card.cleaned_data["name"],
        area=card.cleaned_data["area"],
        filetype=card.cleaned_data["filetype"],
        filter=card.cleaned_data["filter"],
        filter_output=card.cleaned_data["filter_output"],
        extend_start=card.cleaned_data["extend_start"],
        input_fourier=card.cleaned_data["input_fourier"],
        output_directory=card.cleaned_data["output_directory"],
        input_directory=card.cleaned_data["input_directory"],
        run_parallel=card.cleaned_data["run_parallel"],
    )

    return year_filter_card


def collate_update_create(name, card):
    cur_card = None
    collate_card = None

    if Collate.objects.filter(name=card.cleaned_data["name"]).exists():
        cur_card = Collate.objects.get(name=card.cleaned_data["name"])

        if cur_card.input_data_directory != card.cleaned_data["input_data_directory"]:
            Collate.input_files.through.objects.filter(
                    collate_id = cur_card.id).delete()

    if item_id:
        if cur_card == None or cur_card.id == int(item_id):
            Collate.objects.filter(id=item_id).update(
                name=card.cleaned_data["name"],
                area=card.cleaned_data["area"],
                mode=card.cleaned_data["mode"],
                # input_files=card.cleaned_data["input_files"],
                output_tile_subdir=card.cleaned_data["output_tile_subdir"],
                input_scale_factor=card.cleaned_data["input_scale_factor"],
                run_parallel=card.cleaned_data["run_parallel"],
                input_data_directory=card.cleaned_data["input_data_directory"],
            )
            collate_card = Collate.objects.get(id=item_id)
    else:
        if cur_card == None:
            collate_card = Collate.objects.create(
                name=card.cleaned_data["name"],
                area=card.cleaned_data["area"],
                mode=card.cleaned_data["mode"],
                # input_files=card.cleaned_data["input_files"],
                output_tile_subdir=card.cleaned_data["output_tile_subdir"],
                input_scale_factor=card.cleaned_data["input_scale_factor"],
                run_parallel=card.cleaned_data["run_parallel"],
                input_data_directory=card.cleaned_data["input_data_directory"],
            )

    if multiple:
        list_id = multiple.split('_')
        for file_id in list_id:
            if delete:
                Collate.input_files.through.objects.filter(
                    listtestfiles_id=file_id,
                    collate_id = collate_card.id
                ).delete()
            else:
                Collate.input_files.through.objects.create(
                    listtestfiles_id=file_id,
                    collate_id =collate_card.id
                )

    return collate_card


def preproc_update_create(name, card):
    preproc_card = PreProc.objects.create(
        name=card.cleaned_data["name"],
        area=card.cleaned_data["area"],
        mode=card.cleaned_data["mode"],
        year_group=card.cleaned_data["year_group"],
        run_parallel=card.cleaned_data["run_parallel"],
        path_spec_location=card.cleaned_data["path_spec_location"],
    )

    return preproc_card


def mergecsv_update_create(name, card):
    mergecsv_card = MergeCSV.objects.create(
        name=card.cleaned_data["name"],
        csv1=card.cleaned_data["csv1"],
        csv2=card.cleaned_data["csv2"],
    )

    return mergecsv_card


def rftrain_update_create(name, card):
    rftrain_card = RFTrain.objects.create(
        name=card.cleaned_data["name"],
        tile_type=card.cleaned_data["tile_type"],
        number_of_trees=card.cleaned_data["number_of_trees"],
        number_of_thread=card.cleaned_data["number_of_thread"],
        number_of_variable=card.cleaned_data["number_of_variable"],
        training=card.cleaned_data["training"],
        value=card.cleaned_data["value"],
        config_file=card.cleaned_data["config_file"],
        output_tile_subdir=card.cleaned_data["output_tile_subdir"],
        input_scale_factor=card.cleaned_data["input_scale_factor"],
        run_parallel=card.cleaned_data["run_parallel"],
    )

    return rftrain_card


def randomforest_update_create(name, card):
    randomforest_card = RandomForest.objects.create(
        name=card.cleaned_data["name"],
        aoi_name=card.cleaned_data["aoi_name"],
        satellite=card.cleaned_data["satellite"],
        param_set=card.cleaned_data["param_set"],
        run_set=card.cleaned_data["run_set"],
        model=card.cleaned_data["model"],
        mvrf=card.cleaned_data["mvrf"],
    )

    return randomforest_card


def calcstats_update_create(name, card):
    calcstats_card = CalcStats.objects.create(
        name=card.cleaned_data["name"],
        output_tile_subdir=card.cleaned_data["output_tile_subdir"],
        year_group=card.cleaned_data["year_group"],
        area=card.cleaned_data["area"],
        period=card.cleaned_data["period"],
        doy_variable=doy_variable,
        filter=card.cleaned_data["filter"],
        filter_out=filter_out,
        input_fourier=card.cleaned_data["input_fourier"],
        out_dir=card.cleaned_data["out_dir"],
        run_parallel=card.cleaned_data["run_parallel"],
        path_spec_location=card.cleaned_data["path_spec_location"],
    )

    return calcstats_card
