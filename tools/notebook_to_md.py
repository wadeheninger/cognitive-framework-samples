def notebook_to_md(nbfile, output_dir):
    import nbformat, nbconvert, os
    from collections import OrderedDict
    
    nb = nbformat.read(nbfile, as_version=nbformat.NO_CONVERT)

    dir_name, nb_name = os.path.split(nbfile)
    base_nb_name      = os.path.splitext(nb_name)[0]    

    exporter = nbconvert.get_exporter("markdown")
    resources = {'output_files_dir': base_nb_name + "_files", "build_dir": output_dir}
    
    mdtext, resources = nbconvert.export(exporter, nb=nb, resources=resources)

    # Handle metadata specific to docs.microsoft.com
    meta = nb["metadata"].get("ms_docs_meta", {})
    docs_meta = OrderedDict()
    for key in ['title', 'description', 'services', 'author', 'manager',  'ms.service', 'ms.technology', 'ms.topic', 'ms.date', 'ms.author']:
        if key in meta:
            docs_meta[key] = meta[key]

    if len(docs_meta) > 0:
        docs_meta_md = '\n'.join(['---'] + [':'.join(kv) for kv in docs_meta.items()] + ['---'])
        mdtext = docs_meta_md + '\n' + mdtext

    writer = nbconvert.writers.FilesWriter()
    writer.write(mdtext, resources, base_nb_name)


if __name__ == "__main__":
    import argparse, os
    parser = argparse.ArgumentParser()
    parser.add_argument("nbfile")
    parser.add_argument("-o", "--output-dir", default=os.getcwd())
    args = parser.parse_args()
    notebook_to_md(args.nbfile, args.output_dir)
    
    
    
