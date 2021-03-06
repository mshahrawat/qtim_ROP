import qtim_ROP
if __name__ == '__main__':

    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-c', '--config', dest='config', required=True)
    parser.add_argument('-n', '--n-folds', dest='n_folds', default=1)
    parser.add_argument('-o', '--out-dir', dest='out_dir', default=None, type=int)
    parser.add_argument('-e', '--exclusions', dest='exclusions', default=None)
    args = parser.parse_args()

    pipeline = qtim_ROP.preprocessing.preprocess_cross_val.\
        Pipeline(args.config, n_folds=args.n_folds, out_dir=args.out_dir, exclusions=args.exclusions)
    pipeline.run()
