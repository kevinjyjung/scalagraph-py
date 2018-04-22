import scalagraph as sg


def main():
    # params
    batch_size = 1
    num_samples = [2, 3, 4]

    # build query graph
    sg_batch = sg.op.Next(batch_size)()
    sg_s1 = sg.op.Sample(num_samples[0])(sg_batch)
    sg_s2 = sg.op.Sample(num_samples[1])(sg_s1)
    sg_s3 = sg.op.Sample(num_samples[2])(sg_s2)

    # outputs
    sg_outs = [sg_batch, sg_s1, sg_s2, sg_s3]

    # run
    with sg.Session() as sess:
        outs = sess.run(sg_outs)
        [print(o) for o in outs]


if __name__ == '__main__':
    main()
