# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404

from cards.models import (QRF, RFScore, Remap,
                          YearFilter, Collate, PreProc,
                          MergeCSV, RFTrain, RandomForest,
                          CalcStats)
from core.utils import get_copy_name


def create_copycard(card, card_type):
    copy_card_func = COPY_CARD[card_type]
    new_copy_card = copy_card_func(card)
    return new_copy_card


def get_copy_name_card(name, model):
    card_count = model.objects.all().count()
    copy_name_card = get_copy_name(name)
    new_name_card = '{0}*cp{1}'.format(copy_name_card, card_count)

    return new_name_card


def qrf_copy(card):
    name = get_copy_name_card(card, QRF)
    cur_card = get_object_or_404(QRF, name=card)
    qrf_card = QRF.objects.create(
        name=name,
        interval=cur_card.interval,
        number_of_trees=cur_card.number_of_trees,
        number_of_threads=cur_card.number_of_threads,
        directory=cur_card.directory,
    )

    return qrf_card


def rfscore_copy(card):
    name = get_copy_name_card(card, RFScore)
    cur_card = get_object_or_404(RFScore, name=card)
    rfscore_card = RFScore.objects.create(
        name=name,
        area=cur_card.area,
        year_group=cur_card.year_group,
        bias_corrn=cur_card.bias_corrn,
        number_of_threads=cur_card.number_of_threads,
        QRFopts=cur_card.QRFopts,
        ref_target=cur_card.ref_target,
        clean_name=cur_card.clean_name,
        run_parallel=cur_card.run_parallel,
    )

    return rfscore_card


def remap_copy(card):
    name = get_copy_name_card(card, Remap)
    cur_card = get_object_or_404(Remap, name=card)
    remap_card = Remap.objects.create(
        name=name,
        run_parallel=cur_card.run_parallel,
        file_spec=cur_card.file_spec,
        roi=cur_card.roi,
        year_group=cur_card.year_group,
        model_name=cur_card.model_name,
        output_root=cur_card.output_root,
        output_suffix=cur_card.output_suffix,
        scale=cur_card.scale,
        output=cur_card.output,
        color_table=cur_card.color_table,
        refstats_file=cur_card.refstats_file,
        refstats_scale=cur_card.refstats_scale,
        conditional_mean=cur_card.conditional_mean,
        conditional_min=cur_card.conditional_min,
        conditional_median=cur_card.conditional_median,
        conditional_max=cur_card.conditional_max,
        lower_quartile=cur_card.lower_quartile,
        upper_quartile=cur_card.upper_quartile,
    )

    return remap_card


def yearfilter_copy(card):
    name = get_copy_name_card(card, YearFilter)
    cur_card = get_object_or_404(YearFilter, name=card)
    year_filter_card = YearFilter.objects.create(
        name=name,
        area=cur_card.area,
        filetype=cur_card.filetype,
        filter=cur_card.filter,
        filter_output=cur_card.filter_output,
        extend_start=cur_card.extend_start,
        input_fourier=cur_card.input_fourier,
        output_directory=cur_card.output_directory,
        input_directory=cur_card.input_directory,
        run_parallel=cur_card.run_parallel,
    )

    return year_filter_card


def collate_copy(card):
    name = get_copy_name_card(card, Collate)
    cur_card = get_object_or_404(Collate, name=card)
    input_files = Collate.input_files.through.objects.filter(
                        collate_id = cur_card.id
                    )
    collate_card = Collate.objects.create(
        name=name,
        area=cur_card.area,
        mode=cur_card.mode,
        output_tile_subdir=cur_card.output_tile_subdir,
        input_scale_factor=cur_card.input_scale_factor,
        run_parallel=cur_card.run_parallel,
        input_data_directory=cur_card.input_data_directory,
    )

    if input_files:
        for n in input_files:
            Collate.input_files.through.objects.create(
                listtestfiles_id=n.listtestfiles_id,
                collate_id =collate_card.id
            )

    return collate_card


def preproc_copy(card):
    name = get_copy_name_card(card, PreProc)
    cur_card = get_object_or_404(PreProc, name=card)
    preproc_card = PreProc.objects.create(
        name=name,
        area=cur_card.area,
        mode=cur_card.mode,
        year_group=cur_card.year_group,
        run_parallel=cur_card.run_parallel,
        path_spec_location=cur_card.path_spec_location,
    )

    return preproc_card


def mergecsv_copy(card):
    name = get_copy_name_card(card, MergeCSV)
    cur_card = get_object_or_404(MergeCSV, name=card)
    mergecsv_card = MergeCSV.objects.create(
        name=name,
        csv1=cur_card.csv1,
        csv2=cur_card.csv2,
    )

    return mergecsv_card


def rftrain_copy(card):
    name = get_copy_name_card(card, RFTrain)
    cur_card = get_object_or_404(RFTrain, name=card)
    rftrain_card = RFTrain.objects.create(
        name=name,
        tile_type=cur_card.tile_type,
        number_of_trees=cur_card.number_of_trees,
        number_of_thread=cur_card.number_of_thread,
        number_of_variable=cur_card.number_of_variable,
        training=cur_card.training,
        value=cur_card.value,
        config_file=cur_card.config_file,
        output_tile_subdir=cur_card.output_tile_subdir,
        input_scale_factor=cur_card.input_scale_factor,
        run_parallel=cur_card.run_parallel,
    )

    return rftrain_card


def randomforest_copy(card):
    name = get_copy_name_card(card, RandomForest)
    cur_card = get_object_or_404(RandomForest, name=card)
    randomforest_card = RandomForest.objects.create(
        name=name,
        aoi_name=cur_card.aoi_name,
        satellite=cur_card.satellite,
        param_set=cur_card.param_set,
        run_set=cur_card.run_set,
        model=cur_card.model,
        mvrf=cur_card.mvrf,
    )

    return randomforest_card


def calcstats_copy(card):
    name = get_copy_name_card(card, CalcStats)
    cur_card = get_object_or_404(CalcStats, name=card)
    calcstats_card = CalcStats.objects.create(
        name=name,
        output_tile_subdir=cur_card.output_tile_subdir,
        year_group=cur_card.year_group,
        area=cur_card.area,
        period=cur_card.period,
        doy_variable=cur_card.doy_variable,
        filter=cur_card.filter,
        filter_out=cur_card.filter_out,
        input_fourier=cur_card.input_fourier,
        out_dir=cur_card.out_dir,
        run_parallel=cur_card.run_parallel,
        path_spec_location=cur_card.path_spec_location,
    )

    return calcstats_card


COPY_CARD = {
    'qrf': qrf_copy,
    'rfscore': rfscore_copy,
    'remap': remap_copy,
    'yearfilter': yearfilter_copy,
    'collate': collate_copy,
    'preproc': preproc_copy,
    'mergecsv': mergecsv_copy,
    'rftrain': rftrain_copy,
    'randomforest': randomforest_copy,
    'calcstats': calcstats_copy
}
