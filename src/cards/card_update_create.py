# -*- coding: utf-8 -*-
from cards.models import (QRF, RFScore, Remap,
                          YearFilter, Collate, PreProc,
                          MergeCSV, RFTrain, RandomForest,
                          CalcStats)
from gsi.models import ListTestFiles


def qrf_update_create(form, item_id=None):
    cur_card = None
    qrf_card = None

    if QRF.objects.filter(name=form.cleaned_data["name"]).exists():
        cur_card = QRF.objects.get(name=form.cleaned_data["name"])

    if item_id:
        if cur_card == None or cur_card.id == int(item_id):
            QRF.objects.filter(id=item_id).update(
                name=form.cleaned_data["name"],
                interval=form.cleaned_data["interval"],
                number_of_trees=form.cleaned_data["number_of_trees"],
                number_of_threads=form.cleaned_data["number_of_threads"],
                directory=form.cleaned_data["directory"],
            )
            qrf_card = QRF.objects.get(id=item_id)
    else:
        if cur_card == None:
            qrf_card = QRF.objects.create(
                name=form.cleaned_data["name"],
                interval=form.cleaned_data["interval"],
                number_of_trees=form.cleaned_data["number_of_trees"],
                number_of_threads=form.cleaned_data["number_of_threads"],
                directory=form.cleaned_data["directory"],
            )

    return qrf_card


def rfscore_update_create(form, item_id=None):
    cur_card = None
    rfscore_card = None

    if RFScore.objects.filter(name=form.cleaned_data["name"]).exists():
        cur_card = RFScore.objects.get(name=form.cleaned_data["name"])

    if item_id:
        if cur_card == None or cur_card.id == int(item_id):
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
        if cur_card == None:
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
    cur_card = None
    remap_card = None

    if Remap.objects.filter(name=form.cleaned_data["name"]).exists():
        cur_card = Remap.objects.get(name=form.cleaned_data["name"])

    if item_id:
        if cur_card == None or cur_card.id == int(item_id):
            Remap.objects.filter(id=item_id).update(
                name=form.cleaned_data["name"],
                run_parallel=form.cleaned_data["run_parallel"],
                file_spec=form.cleaned_data["file_spec"],
                roi=form.cleaned_data["roi"],
                year_group=form.cleaned_data["year_group"],
                output_root=form.cleaned_data["output_root"],
                output_suffix=form.cleaned_data["output_suffix"],
                scale=form.cleaned_data["scale"],
                output=form.cleaned_data["output"],
                color_table=form.cleaned_data["color_table"],
                refstats_file=form.cleaned_data["refstats_file"],
                refstats_scale=form.cleaned_data["refstats_scale"],
                conditional_mean=form.cleaned_data["conditional_mean"],
                conditional_min=form.cleaned_data["conditional_min"],
                conditional_median=form.cleaned_data["conditional_median"],
                conditional_max=form.cleaned_data["conditional_max"],
                lower_quartile=form.cleaned_data["lower_quartile"],
                upper_quartile=form.cleaned_data["upper_quartile"],
            )
            remap_card = Remap.objects.get(id=item_id)
    else:
        if cur_card == None:
            remap_card = Remap.objects.create(
                name=form.cleaned_data["name"],
                run_parallel=form.cleaned_data["run_parallel"],
                file_spec=form.cleaned_data["file_spec"],
                roi=form.cleaned_data["roi"],
                year_group=form.cleaned_data["year_group"],
                output_root=form.cleaned_data["output_root"],
                output_suffix=form.cleaned_data["output_suffix"],
                scale=form.cleaned_data["scale"],
                output=form.cleaned_data["output"],
                color_table=form.cleaned_data["color_table"],
                refstats_file=form.cleaned_data["refstats_file"],
                refstats_scale=form.cleaned_data["refstats_scale"],
                conditional_mean=form.cleaned_data["conditional_mean"],
                conditional_min=form.cleaned_data["conditional_min"],
                conditional_median=form.cleaned_data["conditional_median"],
                conditional_max=form.cleaned_data["conditional_max"],
                lower_quartile=form.cleaned_data["lower_quartile"],
                upper_quartile=form.cleaned_data["upper_quartile"],
            )

    return remap_card


def year_filter_update_create(form, item_id=None):
    cur_card = None
    year_filter_card = None

    if YearFilter.objects.filter(name=form.cleaned_data["name"]).exists():
        cur_card = YearFilter.objects.get(name=form.cleaned_data["name"])

    if item_id:
        if cur_card == None or cur_card.id == int(item_id):
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
        if cur_card == None:
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


def collate_update_create(form, item_id=None, multiple=None, delete=False):
    cur_card = None
    collate_card = None

    if Collate.objects.filter(name=form.cleaned_data["name"]).exists():
        cur_card = Collate.objects.get(name=form.cleaned_data["name"])

        if cur_card.input_data_directory != form.cleaned_data["input_data_directory"]:
            Collate.input_files.through.objects.filter(
                    collate_id = cur_card.id).delete()

    if item_id:
        if cur_card == None or cur_card.id == int(item_id):
            Collate.objects.filter(id=item_id).update(
                name=form.cleaned_data["name"],
                area=form.cleaned_data["area"],
                mode=form.cleaned_data["mode"],
                # input_files=form.cleaned_data["input_files"],
                output_tile_subdir=form.cleaned_data["output_tile_subdir"],
                input_scale_factor=form.cleaned_data["input_scale_factor"],
                run_parallel=form.cleaned_data["run_parallel"],
                input_data_directory=form.cleaned_data["input_data_directory"],
            )
            collate_card = Collate.objects.get(id=item_id)
    else:
        if cur_card == None:
            collate_card = Collate.objects.create(
                name=form.cleaned_data["name"],
                area=form.cleaned_data["area"],
                mode=form.cleaned_data["mode"],
                # input_files=form.cleaned_data["input_files"],
                output_tile_subdir=form.cleaned_data["output_tile_subdir"],
                input_scale_factor=form.cleaned_data["input_scale_factor"],
                run_parallel=form.cleaned_data["run_parallel"],
                input_data_directory=form.cleaned_data["input_data_directory"],
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


def preproc_update_create(form, item_id=None):
    cur_card = None
    preproc_card = None

    if PreProc.objects.filter(name=form.cleaned_data["name"]).exists():
        cur_card = PreProc.objects.get(name=form.cleaned_data["name"])

    if item_id:
        if cur_card == None or cur_card.id == int(item_id):
            PreProc.objects.filter(id=item_id).update(
                name=form.cleaned_data["name"],
                area=form.cleaned_data["area"],
                mode=form.cleaned_data["mode"],
                year_group=form.cleaned_data["year_group"],
                run_parallel=form.cleaned_data["run_parallel"],
            )
            preproc_card = PreProc.objects.get(id=item_id)
    else:
        if cur_card == None:
            preproc_card = PreProc.objects.create(
                name=form.cleaned_data["name"],
                area=form.cleaned_data["area"],
                mode=form.cleaned_data["mode"],
                year_group=form.cleaned_data["year_group"],
                run_parallel=form.cleaned_data["run_parallel"],
            )

    return preproc_card


def mergecsv_update_create(form, item_id=None):
    cur_card = None
    mergecsv_card = None

    if MergeCSV.objects.filter(name=form.cleaned_data["name"]).exists():
        cur_card = MergeCSV.objects.get(name=form.cleaned_data["name"])

    if item_id:
        if cur_card == None or cur_card.id == int(item_id):
            MergeCSV.objects.filter(id=item_id).update(
                name=form.cleaned_data["name"],
                csv1=form.cleaned_data["csv1"],
                csv2=form.cleaned_data["csv2"],
            )
            mergecsv_card = MergeCSV.objects.get(id=item_id)
    else:
        if cur_card == None:
            mergecsv_card = MergeCSV.objects.create(
                name=form.cleaned_data["name"],
                csv1=form.cleaned_data["csv1"],
                csv2=form.cleaned_data["csv2"],
            )

    return mergecsv_card


def rftrain_update_create(form, item_id=None):
    cur_card = None
    rftrain_card = None

    if RFTrain.objects.filter(name=form.cleaned_data["name"]).exists():
        cur_card = RFTrain.objects.get(name=form.cleaned_data["name"])

    if item_id:
        if cur_card == None or cur_card.id == int(item_id):
            RFTrain.objects.filter(id=item_id).update(
                name=form.cleaned_data["name"],
                tile_type=form.cleaned_data["tile_type"],
                number_of_trees=form.cleaned_data["number_of_trees"],
                number_of_thread=form.cleaned_data["number_of_thread"],
                number_of_variable=form.cleaned_data["number_of_variable"],
                training=form.cleaned_data["training"],
                value=form.cleaned_data["value"],
                config_file=form.cleaned_data["config_file"],
                output_tile_subdir=form.cleaned_data["output_tile_subdir"],
                input_scale_factor=form.cleaned_data["input_scale_factor"],
                run_parallel=form.cleaned_data["run_parallel"],
            )
            rftrain_card = RFTrain.objects.get(id=item_id)
    else:
        if cur_card == None:
            rftrain_card = RFTrain.objects.create(
                name=form.cleaned_data["name"],
                tile_type=form.cleaned_data["tile_type"],
                number_of_trees=form.cleaned_data["number_of_trees"],
                number_of_thread=form.cleaned_data["number_of_thread"],
                number_of_variable=form.cleaned_data["number_of_variable"],
                training=form.cleaned_data["training"],
                value=form.cleaned_data["value"],
                config_file=form.cleaned_data["config_file"],
                output_tile_subdir=form.cleaned_data["output_tile_subdir"],
                input_scale_factor=form.cleaned_data["input_scale_factor"],
                run_parallel=form.cleaned_data["run_parallel"],
            )

    return rftrain_card


def randomforest_update_create(form, item_id=None):
    cur_card = None
    randomforest_card = None

    if RandomForest.objects.filter(name=form.cleaned_data["name"]).exists():
        cur_card = RandomForest.objects.get(name=form.cleaned_data["name"])

    if item_id:
        if cur_card == None or cur_card.id == int(item_id):
            RandomForest.objects.filter(id=item_id).update(
                name=form.cleaned_data["name"],
                aoi_name=form.cleaned_data["aoi_name"],
                satellite=form.cleaned_data["satellite"],
                param_set=form.cleaned_data["param_set"],
                run_set=form.cleaned_data["run_set"],
                model=form.cleaned_data["model"],
                mvrf=form.cleaned_data["mvrf"],
            )
            randomforest_card = RandomForest.objects.get(id=item_id)
    else:
        if cur_card == None:
            randomforest_card = RandomForest.objects.create(
                name=form.cleaned_data["name"],
                aoi_name=form.cleaned_data["aoi_name"],
                satellite=form.cleaned_data["satellite"],
                param_set=form.cleaned_data["param_set"],
                run_set=form.cleaned_data["run_set"],
                model=form.cleaned_data["model"],
                mvrf=form.cleaned_data["mvrf"],
            )

    return randomforest_card


def calcstats_update_create(form, item_id=None):
    cur_card = None
    calcstats_card = None
    filter_out = form.cleaned_data["filter_out"]
    doy_variable = form.cleaned_data["doy_variable"]

    if CalcStats.objects.filter(name=form.cleaned_data["name"]).exists():
        cur_card = CalcStats.objects.get(name=form.cleaned_data["name"])

    if form.cleaned_data["period"] != 'doy':
        doy_variable = ''

    if form.cleaned_data["filter_out"] == 'select':
        filter_out = ''

    if item_id:
        if cur_card == None or cur_card.id == int(item_id):
            CalcStats.objects.filter(id=item_id).update(
                name=form.cleaned_data["name"],
                output_tile_subdir=form.cleaned_data["output_tile_subdir"],
                year_group=form.cleaned_data["year_group"],
                period=form.cleaned_data["period"],
                doy_variable=doy_variable,
                filter=form.cleaned_data["filter"],
                filter_out=filter_out,
                input_fourier=form.cleaned_data["input_fourier"],
                out_dir=form.cleaned_data["out_dir"],
            )
            calcstats_card = CalcStats.objects.get(id=item_id)
    else:
        if cur_card == None:
            calcstats_card = CalcStats.objects.create(
                name=form.cleaned_data["name"],
                output_tile_subdir=form.cleaned_data["output_tile_subdir"],
                year_group=form.cleaned_data["year_group"],
                period=form.cleaned_data["period"],
                doy_variable=doy_variable,
                filter=form.cleaned_data["filter"],
                filter_out=filter_out,
                input_fourier=form.cleaned_data["input_fourier"],
                out_dir=form.cleaned_data["out_dir"],
            )

    return calcstats_card
