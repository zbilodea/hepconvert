from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import uproot


def hadd_1d(destination, file, key, first, *, n_key=None):
    """
    Args:
    destination (path-like): Name of the output file or file path.
    file (ReadOnlyDirectory): ROOT file to read histogram from.
    key (str): key to reference histogram to be added.
    first (bool): if True, special case for first of a certain histogram
        to be added to the new file.
    """
    outfile = uproot.open(destination)
    try:
        hist = file[key] if n_key is None else file[n_key]
    except ValueError:
        msg = "Key missing from {file}"
        raise ValueError(msg) from None
    if first:
        member_data = np.array(
            [
                hist.member("fEntries"),
                hist.member("fTsumw"),
                hist.member("fTsumw2"),
                hist.member("fTsumwx"),
                hist.member("fTsumwx2"),
            ]
        )
        return uproot.writing.identify.to_TH1x(
            hist.member("fName"),
            hist.member("fTitle"),
            hist.values(flow=True),
            *member_data,
            hist.variances(flow=True),
            hist.member("fXaxis"),
        )
    if hist.member("fN") == outfile[key].member("fN"):
        member_data = np.array(
            [
                hist.member("fEntries"),
                hist.member("fTsumw"),
                hist.member("fTsumw2"),
                hist.member("fTsumwx"),
                hist.member("fTsumwx2"),
            ]
        )
        h_sum = uproot.writing.identify.to_TH1x(
            hist.member("fName"),
            hist.member("fTitle"),
            outfile[key].values(flow=True) + hist.values(flow=True),
            *np.add(
                np.array(
                    [
                        outfile[key].member("fEntries"),
                        outfile[key].member("fTsumw"),
                        outfile[key].member("fTsumw2"),
                        outfile[key].member("fTsumwx"),
                        outfile[key].member("fTsumwx2"),
                    ]
                ),
                member_data,
            ),
            outfile[key].variances(flow=True) + hist.variances(flow=True),
            hist.member("fXaxis"),
        )
        outfile.close()
        return h_sum

    msg = "Bins must be the same for histograms to be added, not "
    raise ValueError(
        msg,
        hist.member("fN"),
        " and ",
        outfile[key].member("fN"),
    ) from None


def hadd_2d(destination, file, key, first, *, n_key=None):
    """
    Args:
    destination (path-like): Name of the output file or file path.
    file (ReadOnlyDirectory): ROOT file to read histogram from.
    key (str): key to reference histogram to be added.
    first (bool): if True, special case for first of a certain histogram
        to be added to the new file.
    """
    outfile = uproot.open(destination)
    try:
        hist = file[key] if n_key is None else file[n_key]
    except ValueError:
        msg = "Key missing from {file}"
        raise ValueError(msg) from None
    if first:
        member_data = np.array(
            [
                hist.member("fEntries"),
                hist.member("fTsumw"),
                hist.member("fTsumw2"),
                hist.member("fTsumwx"),
                hist.member("fTsumwx2"),
                hist.member("fTsumwy"),
                hist.member("fTsumwy2"),
                hist.member("fTsumwxy"),
            ]
        )
        return uproot.writing.identify.to_TH2x(
            hist.member("fName"),
            hist.member("fTitle"),
            np.ravel(hist.values(flow=True), order="C"),
            *member_data,
            np.ravel(hist.variances(flow=True), order="C"),
            hist.member("fXaxis"),
            hist.member("fYaxis"),
        )
    if hist.member("fN") == outfile[key].member("fN"):
        member_data = np.array(
            [
                hist.member("fEntries"),
                hist.member("fTsumw"),
                hist.member("fTsumw2"),
                hist.member("fTsumwx"),
                hist.member("fTsumwx2"),
                hist.member("fTsumwy"),
                hist.member("fTsumwy2"),
                hist.member("fTsumwxy"),
            ]
        )

        h_sum = uproot.writing.identify.to_TH2x(
            hist.member("fName"),
            hist.member("fTitle"),
            np.ravel(
                outfile[key].values(flow=True) + hist.values(flow=True), order="C"
            ),
            *np.add(
                np.array(
                    [
                        outfile[key].member("fEntries"),
                        outfile[key].member("fTsumw"),
                        outfile[key].member("fTsumw2"),
                        outfile[key].member("fTsumwx"),
                        outfile[key].member("fTsumwx2"),
                        outfile[key].member("fTsumwy"),
                        outfile[key].member("fTsumwy2"),
                        outfile[key].member("fTsumwxy"),
                    ]
                ),
                member_data,
            ),
            np.ravel(
                outfile[key].variances(flow=True) + hist.variances(flow=True), order="C"
            ),
            hist.member("fXaxis"),
            hist.member("fYaxis"),
        )
        outfile.close()
        return h_sum

    msg = "Bins must be the same for histograms to be added, not "
    raise ValueError(
        msg,
        hist.member("fN"),
        " and ",
        outfile[key].member("fN"),
    ) from None


def hadd_3d(destination, file, key, first, *, n_key=None):
    """
    Args:
    destination (path-like): Name of the output file or file path.
    file (ReadOnlyDirectory): ROOT file to read histogram from.
    key (str): key to reference histogram to be added.
    first (bool): if True, special case for first of a certain histogram
        to be added to the new file.
    """
    outfile = uproot.open(destination)
    try:
        hist = file[key] if n_key is None else file[n_key]
    except ValueError:
        msg = "Key missing from {file}"
        raise ValueError(msg) from None
    if first:
        member_data = np.array(
            [
                hist.member("fEntries"),
                hist.member("fTsumw"),
                hist.member("fTsumw2"),
                hist.member("fTsumwx"),
                hist.member("fTsumwx2"),
                hist.member("fTsumwy"),
                hist.member("fTsumwy2"),
                hist.member("fTsumwxy"),
                hist.member("fTsumwz"),
                hist.member("fTsumwz2"),
                hist.member("fTsumwxz"),
                hist.member("fTsumwyz"),
            ]
        )
        return uproot.writing.identify.to_TH3x(
            hist.member("fName"),
            hist.member("fTitle"),
            np.ravel(hist.values(flow=True), order="C"),
            *member_data,
            np.ravel(hist.variances(flow=True), order="C"),
            hist.member("fXaxis"),
            hist.member("fYaxis"),
            hist.member("fZaxis"),
        )
    if hist.member("fN") == outfile[key].member("fN"):
        member_data = np.add(
            np.array(
                [
                    hist.member("fEntries"),
                    hist.member("fTsumw"),
                    hist.member("fTsumw2"),
                    hist.member("fTsumwx"),
                    hist.member("fTsumwx2"),
                    hist.member("fTsumwy"),
                    hist.member("fTsumwy2"),
                    hist.member("fTsumwxy"),
                    hist.member("fTsumwz"),
                    hist.member("fTsumwz2"),
                    hist.member("fTsumwxz"),
                    hist.member("fTsumwyz"),
                ]
            ),
            np.array(
                [
                    hist.member("fEntries"),
                    outfile[key].member("fTsumw"),
                    outfile[key].member("fTsumw2"),
                    outfile[key].member("fTsumwx"),
                    outfile[key].member("fTsumwx2"),
                    outfile[key].member("fTsumwy"),
                    outfile[key].member("fTsumwy2"),
                    outfile[key].member("fTsumwxy"),
                    outfile[key].member("fTsumwz"),
                    outfile[key].member("fTsumwz2"),
                    outfile[key].member("fTsumwxz"),
                    outfile[key].member("fTsumwyz"),
                ]
            ),
        )
        h_sum = uproot.writing.identify.to_TH3x(
            hist.member("fName"),
            hist.member("fTitle"),
            np.ravel(
                outfile[key].values(flow=True) + hist.values(flow=True), order="C"
            ),
            *member_data,
            np.ravel(
                (outfile[key].variances(flow=True) + hist.variances(flow=True)),
                order="C",
            ),
            hist.member("fXaxis"),
            hist.member("fYaxis"),
            hist.member("fZaxis"),
        )
        outfile.close()
        return h_sum

    msg = "Bins must be the same for histograms to be added, not "
    raise ValueError(
        msg,
        hist.member("fN"),
        " and ",
        outfile[key].member("fN"),
    ) from None


def hadd(
    destination,
    files,
    *,
    force=True,
    append=False,
    compression="lz4",
    compression_level=1,
    skip_bad_files=False,
    union=True,
    same_names=False,
):
    """
    Args:
        destination (path-like): Name of the output file or file path.
        files (Str or list of str): List of local ROOT files to read histograms from.
            May contain glob patterns.
        force (bool): If True, overwrites destination file if it exists. Force and append
            cannot both be True.
        append (bool): If True, appends histograms to an existing file. Force and append
            cannot both be True.
        compression (str): Sets compression level for root file to write to. Can be one of
            "ZLIB", "LZMA", "LZ4", or "ZSTD". By default the compression algorithm is "LZ4".
        compression_level (int): Use a compression level particular to the chosen compressor.
            By default the compression level is 1.
        skip_bad_files (bool): If True, skips corrupt or non-existent files without exiting.
        max_opened_files (int): Limits the number of files to be open at the same time. If 0,
            this gets set to system limit.
        union (bool): If True, adds the histograms that have the same name and copies all others
            to the new file.
        same_names (bool): If True, only adds together histograms which have the same name (key). If False,
            histograms are added together based on TTree structure (bins must be equal).

    Adds together histograms from local ROOT files of a collection of ROOT files, and writes them to
        a new or existing ROOT file.

        >>> odapt.add_histograms("destination.root", ["file1_to_hadd.root", "file2_to_hadd.root"])

    """
    if compression in ("ZLIB", "zlib"):
        compression_code = uproot.const.kZLIB
    elif compression in ("LZMA", "lzma"):
        compression_code = uproot.const.kLZMA
    elif compression in ("LZ4", "lz4"):
        compression_code = uproot.const.kLZ4
    elif compression in ("ZSTD", "zstd"):
        compression_code = uproot.const.kZSTD
    else:
        msg = f"unrecognized compression algorithm: {compression}. Only ZLIB, LZMA, LZ4, and ZSTD are accepted."
        raise ValueError(msg)
    p = Path(destination)
    if Path.is_file(p):
        if not force and not append:
            raise FileExistsError
        if force and append:
            msg = "Cannot append to a new file. Either force or append can be true."
            raise ValueError(msg)
        file_out = uproot.recreate(
            destination,
            compression=uproot.compression.Compression.from_code_pair(
                compression_code, compression_level
            ),
        )
    else:
        if append:
            raise FileNotFoundError(
                "File %s" + destination + " not found. File must exist to append."
            )
        file_out = uproot.recreate(
            destination,
            compression=uproot.compression.Compression.from_code_pair(
                compression_code, compression_level
            ),
        )
    
    if not isinstance(files, list):
        path = Path(files)
        files = sorted(path.glob("**/*.root"))

    if len(files) <= 1:
        msg = "Cannot hadd one file. Use root_to_root to copy a ROOT file."
        raise ValueError(msg) from None

    with uproot.open(files[0]) as file:
        keys = file.keys(filter_classname="TH[1|2|3][I|S|F|D|C]", cycle=False)
    if same_names:
        if union:
            for i, _value in enumerate(files[1:]):
                with uproot.open(files[i]) as file:
                    keys = np.union1d(
                        keys,
                        file.keys(filter_classname="TH[1|2|3][I|S|F|D|C]", cycle=False),
                    )
                    all_keys = np.union1d(files.keys(), keys)
        else:
            for i, _value in enumerate(files[1:]):
                with uproot.open(files[i]) as file:
                    keys = np.intersect1d(
                        keys,
                        file.keys(filter_classname="TH[1|2|3][I|S|F|D|C]", cycle=False),
                    )
                    all_keys = np.intersect1d(files.keys(), keys)
    else:
        keys = file.keys(filter_classname="TH[1|2|3][I|S|F|D|C]", cycle=False)

    first = True
    for input_file in files:
        p = Path(input_file)
        if Path.is_file(p):
            file_out = uproot.update(destination)
        else:
            file_out = uproot.recreate(
                destination,
                compression=uproot.compression.Compression.from_code_pair(
                    compression_code, compression_level
                ),
            )

        try:
            file = uproot.open(input_file)
        except FileNotFoundError:
            if skip_bad_files:
                continue
            msg = "File: {input_file} does not exist or is corrupt."
            raise FileNotFoundError(msg) from None
        if same_names:
            for key in keys:
                try:
                    file[key]
                except ValueError:
                    if not union:
                        continue
                    msg = "Union key filter error."
                    raise ValueError(msg) from None
                if len(file[key].axes) == 1:
                    h_sum = hadd_1d(destination, file, key, first)

                elif len(file[key].axes) == 2:
                    h_sum = hadd_2d(destination, file, key, first)

                else:
                    h_sum = hadd_3d(destination, file, key, first)

        else:
            n_keys = file.keys(filter_classname="TH[1|2|3][I|S|F|D|C]", cycle=False)
            for i, _value in enumerate(keys):
                if len(file[n_keys[i]].axes) == 1:
                    h_sum = hadd_1d(destination, file, keys[i], first, n_key=n_keys[i])

                elif len(file[n_keys[i]].axes) == 2:
                    h_sum = hadd_2d(destination, file, keys[i], first, n_key=n_keys[i])

                else:
                    h_sum = hadd_3d(destination, file, keys[i], first, n_key=n_keys[i])

                if h_sum is not None:
                    file_out[keys[i]] = h_sum

        first = False
        file.close()


def setup_file(all_keys, file, destination):
    with uproot.open(file) as to_copy:
        destination.copy_from(file, filter_name=all_keys)

def main():
    """
    Implementation of cmd-line executables.
    """
    argparser = argparse.ArgumentParser(description="Hadd ROOT histograms with Uproot")
    argparser.add_argument("destination", type=str, help="path of output file")
    argparser.add_argument(
        "input_files",
        type=str,
        nargs="+",
        help="list or directory (glob syntax accepted) of input files",
    )
    argparser.add_argument(
        "-f",
        "--force",
        action="store_true",
        default=True,
        help="force overwrite of output file",
    )
    argparser.add_argument(
        "-a", "--append", action="store", default=False, help="append to existing file"
    )
    argparser.add_argument(
        "-c",
        "--compression",
        action="store",
        default="lz4",
        help="set compression level between 1-9",
    )
    argparser.add_argument(
        "-c[0-9]",
        "--compression_level",
        action="store",
        default=1,
        help="set compression level between 1-9",
    )
    argparser.add_argument(
        "-k",
        "--skip_bad_files",
        action="store",
        default=False,
        help="corrupt or non-existent input files are ignored",
    )
    argparser.add_argument(
        "-u",
        action="union",
        default=True,
        help="all histograms get copied to new file, only those with same name get added",
    )

    args = argparser.parse_args()

    hadd(
        args.destination,
        args.input_file,
        force=args.force,
        append=args.append,
        compression=args.compression,
        compression_level=args.compression_level,
        skip_bad_files=args.skip_bad_files,
        union=args.union,
    )


def merge_files(destination, file1, file2, name, compression): #hadd includes
    # Use tmpdir? Or just do two at a time, tree reduction style...
    import tempfile

    f1 = uproot.open(file1)
    f2 = uproot.open(file2)
    #title must be the same as the file name? maybe is just a tChain thing

    out_file = uproot.recreate(destination, compression)

    for key in f1.keys(out_file, recursive=False):
        class_name = f1[key].class_name()
        if isinstance(class_name, uproot.TTree):
            try:
                if f1[key].name != f2[key].name:
                    print("Names must be the same")
                    recur(out_file, f1[key], f2[key])
            finally: 
                # Write just f1 to file???
                msg = "Files must have similar structure."
                raise ValueError(msg) from None
        elif class_name.startswith("TH[1|2|3][I|S|F|D|C]"):
            hadd_1d(out_file, f1[key], key, first=True, n_key=None) #tree1? does it need to be a file?
        else:
            t1_keys = f1[key].keys()
            t2_keys = f2[key].keys()
            shared_keys = np.intersect1d(t1_keys, t2_keys)
            # out_file.copy_from(ttree1, filter_name=shared_keys, filter_classnames='^(?![Model_TTree]).*$') # worth? good because it's still compressed and faster...but can't guarantee it will be memory friendly?
            # out_file[key] = f1[key]
            # out_file[key] = f2[key]

        # Check if histograms

        # write...
    #   read key - get get class name
    #   inputs(?) = tlist()
    #   if isTree:
    #       obj = obj.CloneTree?
    #       branches = obj.branches
    #   for f2 in files[1:]:
    #       other_obj = f2.getListOfKeys().readObj()
    #       inputs.Add(other_obj)
    #

def recur(out_file, tree1, tree2):
    branches = tree1.branches
    print(branches)
    missing_branches = tree1.branches - tree2.branches

    # get keys for branches? for hadd
    for branch in branches:
        class_name = tree1.class_name()
        if isinstance(class_name, uproot.TTree) and isinstance(tree2.class_name(), uproot.TTree):
            if tree1.name == tree2.name:
                # Iterate here?
                out_file[tree1.name] = branches 
        elif class_name.startswith("TH[1|2|3][I|S|F|D|C]"):
            hadd_1d(out_file, branch, branch.index, first=True, n_key=None) #tree1? does it need to be a file?
        
        else:
            t1_keys = tree1.keys()
            t2_keys = tree2.keys()
            shared_keys = np.intersect1d(t1_keys, t2_keys)
            # out_file.copy_from(ttree1, filter_name=shared_keys, filter_classnames='^(?![Model_TTree]).*$') # worth? good because it's still compressed and faster...but can't guarantee it will be memory friendly?
            # out_file[key] = f1[key]
            # out_file[key] = f2[key]